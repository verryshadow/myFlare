from typing import List

from algorithm import AlgorithmStep
from fhir import generate_fhir_cnf
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


class GenerateFhirCNFStep(AlgorithmStep):
    """
    Generates FHIR Query strings
    """
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.QUERYBUILDING
        default_logger.log_progress_event(instruction)

        return generate_fhir_cnf(data)

