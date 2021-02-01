import json
import os
import time
from argparse import ArgumentParser
from queue import Queue, Empty
from typing import Optional

from flask import Flask as Flask, request, Response
from uuid import uuid4, UUID

import os.path
from requests import RequestException

from worker import instruction_encoder, instruction_decoder
from worker.communication.instruction import Instruction, get_request_file_path, ExecutionState
from worker.communication.processing_event import ProcessingEvent
from worker.threadedworker import ThreadedWorker
from run import run
from xml.etree import ElementTree as ET

app = Flask(__name__)

# Setup worker thread
instruction_queue: 'Queue[Instruction]' = Queue()
event_queue: 'Queue[ProcessingEvent]' = Queue()
worker = ThreadedWorker(instruction_queue, event_queue)


def build_response(result_set, i2b2_request):
    x_result_set = ET.Element("resultSet")
    x_result = ET.Element("patient_count")
    x_result.attrib["value"] = str(len(result_set))
    x_result_set.insert(0, x_result)
    return x_result_set


@app.route("/i2b2", methods=["POST"])
def handle_i2b2_query():
    """
    Synchronous execution API

    takes an I2B2 Query Definition in the body and executes it.
    :return: the number of matching patients found
    """
    print("handling query")
    # Execute and timestamp
    start_time = time.time()
    i2b2_request = request.data.decode("UTF-8")
    try:
        result_set = run(i2b2_request)
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
def create_query():
    """
    Submit a query for execution

    :return: location header containing the url to the result/processing progress
    """
    # Create Instruction
    queue_insertion_time: int = time.time_ns()
    i2b2_request: str = request.data.decode("UTF-8")
    uuid: UUID = uuid4()
    instruction: Instruction = Instruction(i2b2_request, str(uuid), queue_insertion_time)

    # Create execution flag
    with open(instruction.file_path(), "x") as flag:
        flag.write(instruction_encoder.encode(instruction))

    # Queue for execution
    instruction_queue.put(instruction)

    # Respond with location header
    response = app.make_response("")
    response.status_code = 201
    response.headers["Location"] = f"/query/{str(instruction.request_id)}"
    return response


def get_query_from_persistence(query_id: str) -> Optional[Instruction]:
    """
    Fetches a persisted query

    :param query_id:
    :return: if found the Instruction for a given query_id otherwise None
    """
    request_path = get_request_file_path(query_id)

    # Make sure path exists
    if not os.path.exists(request_path):
        return None
    instruction = instruction_decoder.decode(open(request_path, "r").read())
    return instruction


@app.route("/query/<query_id>/status", methods=["GET"])
def handle_query_state(query_id: str):
    """
    Fetches the current processing state of a given query

    :param query_id: id of the query to be looked up
    :return: either 200 and the query state or 400 if query is not found
    """
    query = get_query_from_persistence(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.state.name


@app.route("/query/<query_id>/results", methods=["GET"])
def handle_query_result(query_id: str):
    """
    Fetches the response calculated for a query

    :param query_id: id of the query to fetch the response for
    :return: 404 if not found or the response calculated for the query
    """
    query = get_query_from_persistence(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.response


@app.route("/query/<query_id>", methods=["GET"])
def get_query(query_id: str):
    """
    Fetches the original request data for a given query

    :param query_id:
    :return: 404 if not found or the original request data
    """
    query = get_query_from_persistence(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.request_data, 200


@app.route("/query/", methods=["GET"])
def list_queries():
    # TODO implement this     os.listdir()
    pass


@app.route("/query/<query_id>", methods=["DELETE"])
def delete_query(query_id: str):
    """
    Deletes a persisted query

    :param query_id: id of the query to be deleted
    :return:
    """
    request_path = get_request_file_path(query_id)

    # Make sure path exists
    if not os.path.exists(request_path):
        return "No Query under this id", 404

    os.remove(request_path)
    return f"Successfully deleted {query_id}", 200


def send_events():
    try:
        while True:
            try:
                yield json.dumps(event_queue.get(block=True).__dict__).encode("UTF-8")
            except Empty:
                pass
    # Catch user terminating connection
    except GeneratorExit:
        # FIXME: somehow only gets thrown when attempting to write to an already closed connection
        pass


@app.route('/subscribe', methods=["GET"])
def sse():
    """
    API for server sent events that triggers when a query has been processed

    :return: Stream over all server events
    """
    response = Response(send_events(), mimetype='text/event-stream')
    response.timeout = None
    return response


def refill_queue():
    """
    Refills the instruction queue with instructions from persistence
    """
    base_path = os.environ.get('PERSISTENCE') or "worker/requests"
    for file in os.listdir(base_path):
        # Make sure file is json
        file_ext = os.path.splitext(file)[1]
        if not file_ext == "json":
            continue

        # Decode instruction and skip finished ones
        instruction: Instruction = instruction_decoder.decode(open(f"{base_path}/{file}", "r").read())
        if instruction.state == ExecutionState.Done:
            continue

        instruction_queue.put(instruction)


if __name__ == '__main__':
    # Setup the argument parser
    parser = ArgumentParser(description="FLARE, run feasibility queries via standard HL7 FHIR search requests")
    parser.add_argument("--persistence", type=str, help="path to the folder in which queries should be persisted")
    parser.add_argument("--host", "-H", type=str, help="host on which to listen", default="localhost")
    parser.add_argument("--port", "-P", type=int, help="port on which to listen", default=5000)
    parser.add_argument("--continue", action="store_true", dest="continue_from_persistence")
    args = parser.parse_args()

    # Set application wide persistence folder
    if args.persistence:
        os.environ["PERSISTENCE"] = args.persistence

    if args.continue_from_persistence:
        refill_queue()

    # Start application
    worker.start()
    app.run(args.host, args.port, threaded=True)
