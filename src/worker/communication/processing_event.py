from worker.communication import Instruction
import time


class ProcessingEvent:
    def __init__(self, instruction: Instruction, information: str = None):
        self.timestamp_ns: int = time.time_ns()
        self.instruction_id: str = instruction.request_id
        self.state: str = instruction.state.name
        self.information: str = information
