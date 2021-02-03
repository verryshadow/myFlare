from typing import List

from algorithm import AlgorithmStep
from fhir import generate_fhir_cnf
from worker.communication import Instruction


class GenerateFhirCNFStep(AlgorithmStep):
    def process(self, instruction: Instruction):
        if not instruction.algo_step or type(instruction.algo_step) == List[List[dict]]:
            raise Exception("Executed the FHIR CNF generation without prerequisites having been met")
        instruction.algo_step = generate_fhir_cnf(instruction.algo_step)

