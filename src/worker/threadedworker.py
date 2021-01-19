from queue import Queue
from threading import Thread
import xml.etree.ElementTree as ET
import time
from typing import List, Optional
from os import path

from requests import RequestException

from run import run as process_request
from worker import Instruction, instruction_encoder
from worker.communication.instruction import ExecutionState
from worker.communication.processing_event import ProcessingEvent


def build_response(result_set: List[str]) -> ET.Element:
    # TODO: Add different response modes
    x_result_set = ET.Element("resultSet")
    x_result = ET.Element("patient_count")
    x_result.attrib["value"] = str(len(result_set))
    x_result_set.insert(0, x_result)
    return x_result_set

    #    for result in result_set:
    #       x_result = ET.Element("result")
    #       x_result.attrib["value"] = result
    #       x_result_set.insert(0, x_result)


class ThreadedWorker(Thread):
    """
    Thread that processes instructions passed to it through a shared queue
    """
    def __init__(self, instruction_queue: 'Queue[Instruction]', event_queue: 'Queue[ProcessingEvent]'):
        """

        :param instruction_queue: means of communicating with the thread, Instructions put in the queue will be processed by the worker
        :param event_queue: means of communicating with the server, worker can update the server about changes
        """
        self.instruction_queue: Queue[Instruction] = instruction_queue
        """
        Queue allowing communication from main thread to worker thread
        """
        self.event_queue: Queue[ProcessingEvent] = event_queue
        """
        Queue connecting the worker thread to the main thread
        """
        self.instruction: Optional[Instruction] = None
        """
        Instruction currently processed by the thread
        """
        super().__init__()

    # TODO: implement graceful shutdown
    def run(self):
        while True:
            # Wait for main thread to add instruction to queue
            self.instruction = self.instruction_queue.get(block=True, timeout=None)
            # Skip removed instructions since they cannot be deleted from the Queue
            if self.current_instruction_deleted():
                continue

            # Setup instruction to process
            self.instruction.processing_start_time = time.time_ns()
            self.instruction.state = ExecutionState.Executing

            # Notify queue about event
            event = ProcessingEvent(time.time_ns(), str(self.instruction.request_id), self.instruction.state)
            self.event_queue.put(event)

            # Process instruction
            self.handle()

    def handle(self):
        """
        Processes the current instruction and persists the result
        """
        try:
            # Process instruction and build response
            result_set: List[str] = process_request(self.instruction.request_data)
            x_response = build_response(result_set)
            self.insert_timestamps(x_response)
            response = ET.tostring(x_response).decode("UTF-8")

            # Add response to instruction and persist instruction as done
            self.instruction.response = response
            self.instruction.state = ExecutionState.Done
            self.persist_instruction()

            # Notify server about event
            event = ProcessingEvent(time.time_ns(), str(self.instruction.request_id), self.instruction.state)
            self.event_queue.put(event)

        except RequestException as e:
            return "Connection error with upstream FHIR server", 504

    def insert_timestamps(self, x_response):
        """
        Inserts start_time, queue_time, end_time and delta tags into the xml response
        :param x_response: existing response to add the timestamps to
        """
        end_time = time.time()
        delta = end_time - self.instruction.processing_start_time

        # Create timestamp tags
        x_start_time = ET.Element("start_time")
        x_start_time.attrib["value"] = str(self.instruction.processing_start_time)

        x_queue_time = ET.Element("queue_time")
        x_queue_time.attrib["value"] = str(self.instruction.queue_time)

        x_end_time = ET.Element("end_time")
        x_end_time.attrib["value"] = str(end_time)

        x_delta = ET.Element("delta")
        x_delta.attrib["value"] = str(delta)

        # Insert timestamp tags into response
        x_response.insert(0, x_end_time)
        x_response.insert(0, x_start_time)
        x_response.insert(0, x_delta)

    def persist_instruction(self):
        """
        Encodes instruction into json and writes it to Instruction.file_path()
        """
        with open(self.instruction.file_path(), "w") as file:
            instruction_txt = instruction_encoder.encode(self.instruction)
            file.write(instruction_txt)

    def current_instruction_deleted(self) -> bool:
        """
        checks whether the instruction currently processed has been deleted by the user
        :return: true if Instruction persistence has been removed
        """
        return not path.exists(self.instruction.file_path())
