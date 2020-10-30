import json
from json import JSONDecoder
from json.encoder import JSONEncoder
import time
from uuid import UUID
from enum import Enum

ExecutionState = Enum("ExecutionState", "Queued Executing Aborted Done")


class Instruction:
    def __init__(self, request_data: str, request_id: UUID, queue_time: int,
                 state: ExecutionState = ExecutionState.Queued):
        """
        Creates a new Instruction that can be processed by the worker thread by putting it in the queue

        :param request_data: data contained in the request body
        :param request_id: generated unique id, used to track the request
        :param queue_time: time this got queued
        :param state: Current execution state of the instruction, default is Queued
        """
        self.request_data: str = request_data
        self.response: str = ""
        self.request_id: UUID = request_id
        self.queue_time: int = queue_time
        self.state: ExecutionState = state

    def file_path(self) -> str:
        return f"worker/requests/{self.request_id}.json"


class InstructionEncoder(JSONEncoder):
    """
    Encoder to be used by json.
    """
    def default(self, o: Instruction) -> str:
        obj_repr = {
            "request_data": o.request_data,
            "request_id": str(o.request_id),
            "queue_time": o.queue_time,
            "execution_state": o.state.value
        }
        return json.dumps(obj_repr)


def instruction_decoder_object_hook(o: dict) -> Instruction:
    if "request_data" not in o:
        raise ValueError("Missing required request_data in json object")

    request_data = o["request_data"]
    queue_time = o["queue_time"] if "queue_time" in o else time.time_ns()
    request_id = o["request_id"] if "request_id" in o else -1
    # Todo: check if o.execution_state is valid
    print("called")
    state = ExecutionState[o["execution_state"]] if "execution_state" in o else ExecutionState.Queued
    return Instruction(request_data, request_id, queue_time, state=state)


instruction_encoder = InstructionEncoder()
instruction_decoder = JSONDecoder(object_hook=instruction_decoder_object_hook)


if __name__ == "__main__":
    json = json.load(open("requests/79bc0475-584a-4a2c-8a06-f1d3614f9caf.json", "r"),
                     object_hook=instruction_decoder_object_hook)
    print(json)
