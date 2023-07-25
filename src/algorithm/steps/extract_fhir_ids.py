from algorithm import AlgorithmStep
from myfhir import get_patient_ids_from_bundle
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import LoggingCallback, default_logger


class ExtractFhirIdsStep(AlgorithmStep):
    """
    Replaces the FHIR-Bundles with a set of contained IDs
    """
    def process(self, instruction: Instruction, data: any, callback: LoggingCallback = default_logger):
        instruction.state = ExecutionState.FHIRPARSING
        default_logger.log_progress_event(instruction)

        fhir_query_results = []
        for fhir_disjunction_response in data:
            fhir_cnf_results = []
            for fhir_paged_responses in fhir_disjunction_response:
                page_ids = []
                for fhir_response in fhir_paged_responses:
                    patient_ids = get_patient_ids_from_bundle(fhir_response)
                    page_ids.append(patient_ids)
                fhir_cnf_results.append(page_ids)
            fhir_query_results.append(fhir_cnf_results)
        return fhir_query_results
