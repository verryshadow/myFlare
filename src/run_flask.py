import asyncio
import json
import time
from queue import Queue, Empty
from typing import Optional

from quart import Quart as Flask, request, make_response
from uuid import uuid4, UUID

import os.path
from requests import RequestException

from worker import instruction_encoder, instruction_decoder
from worker.communication.instruction import Instruction, get_request_file_path
from worker.communication.processing_event import ProcessingEvent
from worker.threadedworker import ThreadedWorker
from run import run
from xml.etree import ElementTree as ET

app = Flask(__name__)
instruction_queue: 'Queue[Instruction]' = Queue()
event_queue: 'Queue[ProcessingEvent]' = Queue()


def build_response(result_set, i2b2_request):
    x_result_set = ET.Element("resultSet")
    x_result = ET.Element("patient_count")
    x_result.attrib["value"] = str(len(result_set))
    x_result_set.insert(0, x_result)
    return x_result_set

#    for result in result_set:
#       x_result = ET.Element("result")
#       x_result.attrib["value"] = result
#       x_result_set.insert(0, x_result)


@app.route("/i2b2", methods=["POST"])
def handle_i2b2_query():
    print("handling query")
    # Execute and timestamp
    start_time = time.time()
    i2b2_request = request.data.decode("UTF-8")
    i2b2_query = request.data.decode("UTF-8")
    result_set = run(i2b2_query)
    response = build_response(result_set, i2b2_request)
    try:
        result_set = run(i2b2_query)
        response = build_response(result_set, i2b2_request)
    except RequestException as e:
        return "Connection error with upstream FHIR server", 504

    end_time = time.time()
    delta = end_time - start_time

    # Insert timestamps into result_set
    x_start_time = ET.Element("start_time")
    x_start_time.attrib["value"] = str(start_time)

    x_end_time = ET.Element("end_time")
    x_end_time.attrib["value"] = str(end_time)

    x_delta = ET.Element("delta")
    x_delta.attrib["value"] = str(delta)

    response.insert(0, x_end_time)
    response.insert(0, x_start_time)
    response.insert(0, x_delta)
    response = ET.tostring(response).decode("UTF-8")

    return str(response)


@app.route("/query", methods=["POST"])
async def create_i2b2_query():
    # Create Instruction
    queue_insertion_time: int = time.time_ns()
    print((await request.data).decode("UTF-8"))
    i2b2_request: str = (await request.data).decode("UTF-8")
    uuid: UUID = uuid4()
    instruction: Instruction = Instruction(i2b2_request, uuid, queue_insertion_time)

    # Create execution flag
    with open(instruction.file_path(), "x") as flag:
        flag.write(instruction_encoder.encode(instruction))

    # Queue for execution
    instruction_queue.put(instruction)

    # TODO: Set response link in location header and HTTP CREATED
    response = await app.make_response("")
    response.status_code = 201
    response.headers["Location"] = f"/query/{str(instruction.request_id)}"
    return response


def get_query_from_persistence(query_id: str) -> Optional[Instruction]:
    request_path = get_request_file_path(query_id)

    # Make sure path exists
    if not os.path.exists(request_path):
        return None
    instruction = instruction_decoder.decode(open(request_path, "r").read())
    return instruction


@app.route("/query/<query_id>/status", methods=["GET"])
async def handle_query_state(query_id: str):
    query = get_query_from_persistence(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.state.name


@app.route("/query/<query_id>/results", methods=["GET"])
async def handle_query_result(query_id: str):
    query = get_query_from_persistence(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.response


@app.route("/query/<query_id>", methods=["GET"])
async def get_query(query_id: str):
    query = get_query_from_persistence(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.request_data, 200


@app.route("/query/", methods=["GET"])
async def list_queries():
    # TODO Implement
    pass


@app.route("/query/<query_id>", methods=["DELETE"])
async def delete_query(query_id: str):
    request_path = get_request_file_path(query_id)

    # Make sure path exists
    if not os.path.exists(request_path):
        return "No Query under this id", 404

    os.remove(request_path)
    return f"Successfully deleted {query_id}", 200


@app.route('/subscribe', methods=["GET"])
async def sse():
    async def send_events():
        print("send_events executed")
        while True:
            try:
                yield json.dumps(event_queue.get(block=False).__dict__).encode("UTF-8")
                print("Yielded event")
            except Empty:
                await asyncio.sleep(0.5)

    response = await make_response(
        send_events(),
        {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Transfer-Encoding': 'chunked',
        },
    )
    response.timeout = None
    return response

worker = ThreadedWorker(instruction_queue, event_queue)
worker.start()
app.run("localhost", 5001, threaded=True)
