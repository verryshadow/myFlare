from algorithm import AlgorithmStep
from myfhir import build_result_set_from_query_results
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


class ResolveCNFStep(AlgorithmStep):
    """
    Resolves the CNF of IDs into the final list of IDs that match the query
    """
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.AGGREGATING
        default_logger.log_progress_event(instruction)

        result_set = build_result_set_from_query_results(data)
        return result_set
