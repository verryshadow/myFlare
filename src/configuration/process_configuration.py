from typing import Dict, List

from algorithm.steps.execute_fhir_queries import ExecuteFhirQueriesStep
from algorithm.steps.extract_fhir_ids import ExtractFhirIdsStep
from algorithm.steps.generate_fhir_cnf import GenerateFhirCNFStep
from algorithm.steps.resolve_cnf import ResolveCNFStep
from configuration.io_types import ResponseType
from algorithm import AlgorithmStep
from algorithm.steps import ParseStep


response_algo_steps_map: Dict[ResponseType, List[AlgorithmStep]] = {
    ResponseType.RESULT: [ParseStep(),  GenerateFhirCNFStep(), ExecuteFhirQueriesStep(),
                          ExtractFhirIdsStep(), ResolveCNFStep()],
    ResponseType.INTERNAL: [ParseStep()]
}
"""
Dictionary that maps each implemented ResponseType to the List of steps that have to be executed on the Input
 to achieve the wished result
"""
