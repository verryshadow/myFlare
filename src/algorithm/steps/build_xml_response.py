from typing import List
import xml.etree.ElementTree as Etree
import time

from algorithm import AlgorithmStep
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


def build_response(result_set: List[str]) -> Etree.Element:
    # TODO: Add different response modes
    x_result_set = Etree.Element("resultSet")
    x_result = Etree.Element("patient_count")
    x_result.attrib["value"] = str(len(result_set))
    x_result_set.insert(0, x_result)
    return x_result_set

    #    for result in result_set:
    #       x_result = Etree.Element("result")
    #       x_result.attrib["value"] = result
    #       x_result_set.insert(0, x_result)


def insert_timestamps(x_response, instruction):
    """
    Inserts start_time, queue_time, end_time and delta tags into the xml response
    :param x_response: existing response to add the timestamps to
    """
    end_time = time.time()
    delta = end_time - instruction.processing_start_time

    # Create timestamp tags
    x_start_time = Etree.Element("start_time")
    x_start_time.attrib["value"] = str(instruction.processing_start_time)

    x_queue_time = Etree.Element("queue_time")
    x_queue_time.attrib["value"] = str(instruction.queue_time)

    x_end_time = Etree.Element("end_time")
    x_end_time.attrib["value"] = str(end_time)

    x_delta = Etree.Element("delta")
    x_delta.attrib["value"] = str(delta)

    # Insert timestamp tags into response
    x_response.insert(0, x_end_time)
    x_response.insert(0, x_start_time)
    x_response.insert(0, x_delta)


class BuildXmlResponseStep(AlgorithmStep):
    """
    Builds response of type ResponseType.RESULT
    """
    def process(self, instruction: Instruction, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.RESULTBUILDING
        default_logger.log_progress_event(instruction, information=instruction.response_type.name)

        result_set = instruction.algo_step
        x_response = build_response(result_set)
        insert_timestamps(x_response, instruction)
        response = Etree.tostring(x_response).decode("UTF-8")
        instruction.algo_step = response
