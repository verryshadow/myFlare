from abc import ABC, abstractmethod

from worker.communication import Instruction
from worker.communication.logging_callback import LoggingCallback


class AlgorithmStep(ABC):
    @abstractmethod
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback):
        pass
