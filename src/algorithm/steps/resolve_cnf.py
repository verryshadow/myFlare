from algorithm import AlgorithmStep
from fhir import build_result_set_from_query_results
from worker.communication import Instruction


class ResolveCNFStep(AlgorithmStep):
    def process(self, instruction: Instruction):
        result_set = build_result_set_from_query_results(instruction.algo_step)
        instruction.algo_step = result_set
        return
