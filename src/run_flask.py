import time
from queue import Queue

from flask import Flask, request
from uuid import uuid4, UUID

from worker import instruction_encoder
from worker.instruction import Instruction
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

    return "queued", 200


worker = Worker(instruction_queue)
worker.start()
app.run("localhost", 5000)
