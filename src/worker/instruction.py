from json import JSONDecoder
from json.encoder import JSONEncoder
import time
from uuid import UUID, uuid4
from enum import Enum

ExecutionState = Enum("ExecutionState", "Queued Executing Aborted Done")
"""
Enum allowing Instruction to detail in which stage of execution it currently is
"""


class Instruction:
    def __init__(self, request_data: str, request_id: UUID, queue_time: int,
                 state: ExecutionState = ExecutionState.Queued, processing_start_time: int = 0, response: str = ""):
        """
        Creates a new Instruction that can be processed by the worker thread by putting it in the queue

        :param request_data: Data contained in the request body
        :param request_id: Generated unique id, used to track the request
        :param queue_time: Timestamp this got queued
        :param state: Current execution state of the instruction, default is Queued
        :param processing_start_time: Timestamp worker started processing this
        """
        self.request_data: str = request_data
        """
        Data contained in the request body
        """
        self.response: str = response
        """
        Marshalled response xml
        """
        self.request_id: UUID = request_id
        """
        Generated unique id, used to track the request
        """
        self.queue_time: int = queue_time
        """
        Timestamp this got queued
        """
        self.state: ExecutionState = state
        """
        Current execution state of the instruction
        """
        self.processing_start_time: int = processing_start_time
        """
        Timestamp worker started processing this
        """

    def file_path(self) -> str:
        """
        :return: unique filepath for this instruction based on it's id
        """
        return get_request_file_path(str(self.request_id))


class InstructionEncoder(JSONEncoder):
    """
    Encoder that encodes Instructions to JSON
    """
    def default(self, o: Instruction) -> dict:
        obj_repr = {
            "request_data": o.request_data,
            "response": o.response,
            "request_id": str(o.request_id),
            "queue_time": o.queue_time,
            "processing_start_time": o.processing_start_time,
            "execution_state": o.state.name
        }
        return obj_repr


def instruction_decoder_object_hook(o: dict) -> Instruction:
    """
    Object hook used to create a JSONDecoder that can decode JSON to instruction
    :param o: dictionary containing all relevant data
    :return: Instruction described by the dictionary
    """
    # Make sure required fields are contained
    if "request_data" not in o:
        raise ValueError("Missing required request_data in json object")

    # Read values from dictionary, set default value if they don't exist
    request_data = o["request_data"]
    queue_time = o["queue_time"] if "queue_time" in o else time.time_ns()
    request_id = UUID(o["request_id"]) if "request_id" in o else uuid4()
    # TODO parse response and processing_start_time
    state = ExecutionState.Queued
    if "execution_state" in o:
        # Make sure state exists
        if o["execution_state"] in ExecutionState.__members__:
            state = ExecutionState[o["execution_state"]]
    response = o["response"] if "response" in o else ""
    processing_start_time = o["processing_start_time"] if "processing_start_time" in o else 0

    return Instruction(request_data, request_id, queue_time, state=state, processing_start_time=processing_start_time,
                       response=response)


instruction_encoder: JSONEncoder = InstructionEncoder()
"""
Encodes Instructions into JSON when calling .encode(instruction)
"""
instruction_decoder: JSONDecoder = JSONDecoder(object_hook=instruction_decoder_object_hook)
"""
Decodes JSON into Instructions
"""


def get_request_file_path(request_id: str):
    return f"worker/requests/{request_id}.json"


if __name__ == "__main__":
    # just for personal testing purposes
    json = instruction_decoder.decode(open("requests/195d3614-8e09-40f4-b020-0edabd9b17ec.json", "r").read())
    print(json)
