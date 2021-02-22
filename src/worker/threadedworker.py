import time
from os import path
from queue import Queue
from threading import Thread
from typing import Optional

from requests import RequestException

from run import run as process_request
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState, instruction_encoder
from worker.communication.processing_event import ProcessingEvent


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
            self.instruction.state = ExecutionState.EXECUTING
            self.persist_instruction()

            # Notify queue about event
            event = ProcessingEvent(self.instruction)
            self.event_queue.put(event)

            # Process instruction
            self.handle()

    def handle(self):
        """
        Processes the current instruction and persists the result
        """
        try:
            # Process instruction and build response
            response: str = process_request(self.instruction)

            # Add response to instruction and persist instruction as done
            self.instruction.response = response
            self.instruction.state = ExecutionState.DONE
            self.persist_instruction()

            # Notify server about event
            event = ProcessingEvent(self.instruction)
            self.event_queue.put(event)

        except RequestException:
            return "Connection error with upstream FHIR server", 504

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
