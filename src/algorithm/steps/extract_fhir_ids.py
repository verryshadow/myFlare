from algorithm import AlgorithmStep
from fhir import get_patient_ids_from_bundle
from worker.communication import Instruction


class ExtractFhirIdsStep(AlgorithmStep):
    """
    Replaces the FHIR-Bundles with a set of contained IDs

    :param fhir_cnf_responses: FHIR-Responses in CNF format
    :return: IDs contained in the FHIR-Bundles
    """
    def process(self, instruction: Instruction):
        fhir_query_results = []
        for fhir_disjunction_response in instruction.algo_step:
            fhir_cnf_results = []
            for fhir_paged_responses in fhir_disjunction_response:
                page_ids = []
                for fhir_response in fhir_paged_responses:
                    patient_ids = get_patient_ids_from_bundle(fhir_response)
                    page_ids.append(patient_ids)
                fhir_cnf_results.append(page_ids)
            fhir_query_results.append(fhir_cnf_results)
        instruction.algo_step = fhir_query_results
        return
