from typing import List

from configuration.parser_configuration import syntax_parser_map
from algorithm import AlgorithmStep
from worker.communication import Instruction


class ParseStep(AlgorithmStep):
    def process(self, instruction: Instruction):
        intermediate_query_repr: List[List[dict]] = \
            syntax_parser_map[instruction.query_syntax](instruction.request_data)
        instruction.algo_step = intermediate_query_repr
        return
