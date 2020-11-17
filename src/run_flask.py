import time
from queue import Queue
from typing import Optional

from flask import Flask, request
from uuid import uuid4, UUID

import os.path

from worker import instruction_encoder, instruction_decoder
from worker.instruction import Instruction, get_request_file_path
from worker.worker import Worker

app = Flask(__name__)
instruction_queue: 'Queue[Instruction]' = Queue()


@app.route("/query", methods=["POST"])
def handle_i2b2_query():
    # Create Instruction
    queue_insertion_time: int = time.time_ns()
    i2b2_request: str = request.data.decode("UTF-8")
    uuid: UUID = uuid4()
    instruction: Instruction = Instruction(i2b2_request, uuid, queue_insertion_time)

    # Create execution flag
    with open(instruction.file_path(), "x") as flag:
        flag.write(instruction_encoder.encode(instruction))

    # Queue for execution
    instruction_queue.put(instruction)

    return f"/query/{str(instruction.request_id)}/status", 200


def get_query(query_id: str) -> Optional[Instruction]:
    request_path = get_request_file_path(query_id)

    # Make sure path exists
    if not os.path.exists(request_path):
        return None
    instruction = instruction_decoder.decode(open(request_path, "r").read())
    return instruction


@app.route("/query/<query_id>/status", methods=["GET"])
def handle_query_state(query_id: str):
    query = get_query(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.state.name


@app.route("/query/<query_id>/results", methods=["GET"])
def handle_query_result(query_id: str):
    query = get_query(query_id)
    if query is None:
        return "No Query under this id", 404

    return query.response


worker = Worker(instruction_queue)
worker.start()
app.run("localhost", 5001)
