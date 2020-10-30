from queue import Queue
from threading import Thread
import xml.etree.ElementTree as ET
import time
from typing import List

from requests import RequestException

from run import run as process_request
from worker import Instruction, instruction_encoder
from worker.instruction import ExecutionState


def build_response(result_set: List[str]) -> ET.Element:
    x_result_set = ET.Element("resultSet")
    x_result = ET.Element("patient_count")
    x_result.attrib["value"] = str(len(result_set))
    x_result_set.insert(0, x_result)
    return x_result_set

    #    for result in result_set:
    #       x_result = ET.Element("result")
    #       x_result.attrib["value"] = result
    #       x_result_set.insert(0, x_result)


class Worker(Thread):
    def __init__(self, q: 'Queue[Instruction]'):
        self.q: Queue[Instruction] = q
        self.instruction: Instruction = None
        self.start_time: int = 0
        super().__init__()

    def run(self):
        while True:
            self.instruction = self.q.get(block=True, timeout=None)
            self.start_time = time.time_ns()
            self.instruction.state = ExecutionState.Executing
            self.handle()

    def handle(self):
        try:
            result_set: List[str] = process_request(self.instruction.request_data)
            x_response = build_response(result_set)
            self.insert_timestamps(x_response)
            self.persist_response(x_response)

        except RequestException as e:
            return "Connection error with upstream FHIR server", 504

    def insert_timestamps(self, x_response):
        end_time = time.time()
        delta = end_time - self.start_time

        x_start_time = ET.Element("start_time")
        x_start_time.attrib["value"] = str(self.start_time)

        x_queue_time = ET.Element("queue_time")
        x_queue_time.attrib["value"] = str(self.instruction.queue_time)

        x_end_time = ET.Element("end_time")
        x_end_time.attrib["value"] = str(end_time)

        x_delta = ET.Element("delta")
        x_delta.attrib["value"] = str(delta)

        # Insert timestamps into response
        x_response.insert(0, x_end_time)
        x_response.insert(0, x_start_time)
        x_response.insert(0, x_delta)

    def persist_response(self, x_response):
        response = ET.tostring(x_response).decode("UTF-8")
        self.instruction.response = response
        with open(self.instruction.file_path(), "w") as file:
            instruction_txt = instruction_encoder.encode(self.instruction)
            file.writelines(instruction_txt)
