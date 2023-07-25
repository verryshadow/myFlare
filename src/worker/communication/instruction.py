import os
import pathlib
import time
from enum import Enum
from json import JSONDecoder
from json.encoder import JSONEncoder

from configuration.io_types import QuerySyntax, ResponseType

ExecutionState = Enum("ExecutionState", "QUEUED EXECUTING PARSING MAPPING QUERYBUILDING FHIREXECUTION FHIRPARSING "
                                        "AGGREGATING RESULTBUILDING ABORTED DONE")
"""
Enum allowing Instruction to detail in which stage of execution it currently is
"""


class Instruction:
    def __init__(self, request_data: str, request_id: str, queue_time: int,
                 state: ExecutionState = ExecutionState.QUEUED, processing_start_time: int = 0, response: str = "",
                 query_syntax: QuerySyntax = QuerySyntax.I2B2, response_type: ResponseType = ResponseType.RESULT):
        """
        Creates a new Instruction that can be processed by the worker thread by putting it in the queue

        :param request_data: Data contained in the request body
        :param request_id: Generated unique id, used to track the request
        :param queue_time: Timestamp this got queued
        :param state: Current execution state of the instruction, default is Queued
        :param processing_start_time: Timestamp worker started processing this
        :param query_syntax: Syntax the request is formulated in
        :param response_type Type of response expected by the requesting party
        """

        self.request_data: str = request_data
        """
        Data contained in the request body
        """
        self.response: str = response
        """
        Marshalled response xml
        """
        self.request_id: str = request_id
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
        self.query_syntax: QuerySyntax = query_syntax
        """
        Syntax the request is formulated in
        """
        self.response_type: ResponseType = response_type
        """
        Type of response expected by the requesting party
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
            "request_id": o.request_id,
            "queue_time": o.queue_time,
            "processing_start_time": o.processing_start_time,
            "execution_state": o.state.name,
            "request_type": o.query_syntax.name,
            "response_type": o.response_type.name
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
    request_id = o["request_id"] if "request_id" in o else None
    state = ExecutionState.QUEUED
    if "execution_state" in o:
        # Make sure state exists
        if o["execution_state"] in ExecutionState.__members__:
            state = ExecutionState[o["execution_state"]]
    response = o["response"] if "response" in o else ""
    request_type = QuerySyntax[o["request_type"]] if "request_type" in o else QuerySyntax.I2B2
    response_type = ResponseType[o["response_type"]] if "response_type" in o else ResponseType.RESULT
    processing_start_time = o["processing_start_time"] if "processing_start_time" in o else 0

    return Instruction(request_data, request_id, queue_time, state=state, processing_start_time=processing_start_time,
                       response=response, query_syntax=request_type, response_type=response_type)


instruction_encoder: JSONEncoder = InstructionEncoder()
"""
Encodes Instructions into JSON when calling .encode(instruction)
"""
instruction_decoder: JSONDecoder = JSONDecoder(object_hook=instruction_decoder_object_hook)
"""
Decodes JSON into Instructions
"""


def get_request_file_path(request_id: str):
    base_path = os.environ.get('PERSISTENCE') or "./worker/requests"
    pathlib.Path(base_path).mkdir(0o755, parents=True, exist_ok=True)
    return f"{base_path}/{request_id}.json"


if __name__ == "__main__":
    # just for personal testing purposes
    json = instruction_decoder.decode(open("requests/195d3614-8e09-40f4-b020-0edabd9b17ec.json", "r").read())
    print(json)
