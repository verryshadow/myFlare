from abc import ABC, abstractmethod

from worker.communication import Instruction


class AlgorithmStep(ABC):
    @abstractmethod
    def process(self, instruction: Instruction):
        pass
