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
    def process(self, instruction: Instruction, callback: LoggingCallback = default_logger):
        if not instruction.algo_step or type(instruction.algo_step) == List[List[dict]]:
            raise Exception("Executed the FHIR CNF generation without prerequisites having been met")

        instruction.state = ExecutionState.QUERYBUILDING
        default_logger.log_progress_event(instruction)

        instruction.algo_step = generate_fhir_cnf(instruction.algo_step)

