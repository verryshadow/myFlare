from typing import List

from configuration.parser_configuration import syntax_parser_map
from algorithm import AlgorithmStep
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


class ParseStep(AlgorithmStep):
    """
    Calls the appropriate parser for the given input
    """
    def process(self, instruction: Instruction, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.PARSING
        default_logger.log_progress_event(instruction, information=instruction.query_syntax.name)

        intermediate_query_repr: List[List[dict]] = \
            syntax_parser_map[instruction.query_syntax](instruction.request_data)
        instruction.algo_step = intermediate_query_repr
        return
