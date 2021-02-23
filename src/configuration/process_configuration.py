from typing import Dict, List

from algorithm.steps import ParseStep, BuildInternalResponseStep, BuildXmlResponseStep, ExecuteFhirQueriesStep, \
    ExtractFhirIdsStep, GenerateFhirCNFStep, ResolveCNFStep
from configuration.io_types import ResponseType
from algorithm import AlgorithmStep

response_algo_steps_map: Dict[ResponseType, List[AlgorithmStep]] = {
    ResponseType.RESULT: [ParseStep(),  GenerateFhirCNFStep(), ExecuteFhirQueriesStep(),
                          ExtractFhirIdsStep(), ResolveCNFStep(), BuildXmlResponseStep()],
    ResponseType.INTERNAL: [ParseStep(), GenerateFhirCNFStep(), BuildInternalResponseStep()]
}
"""
Dictionary that maps each implemented ResponseType to the List of steps that have to be executed on the Input
 to achieve the wished result
"""
