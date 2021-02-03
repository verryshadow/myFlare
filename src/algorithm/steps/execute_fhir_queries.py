from algorithm import AlgorithmStep
from fhir import execute_fhir_query
from worker.communication import Instruction


class ExecuteFhirQueriesStep(AlgorithmStep):
    def process(self, instruction: Instruction):
        fhir_cnf_responses = [[execute_fhir_query(query) for query in fhir_disjunction] for fhir_disjunction in
                              instruction.algo_step]
        instruction.algo_step = fhir_cnf_responses
        return
