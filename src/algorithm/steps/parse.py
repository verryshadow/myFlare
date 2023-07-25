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
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.PARSING
        callback.log_progress_event(instruction, information=instruction.query_syntax.name)

        intermediate_query_repr: List[List[List[dict]]] = \
            syntax_parser_map[instruction.query_syntax](data)
        return intermediate_query_repr
