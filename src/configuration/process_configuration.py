from typing import Dict, List

from algorithm.steps import ParseStep, BuildInternalResponseStep, BuildXmlResponseStep, ExecuteFhirQueriesStep, \
    ExtractFhirIdsStep, GenerateFhirCNFStep, ResolveCNFStep
from configuration.io_types import ResponseType
from algorithm import AlgorithmStep


class ProcessConfiguration:
    def __init__(self, steps: List[AlgorithmStep], response_step: AlgorithmStep):
        self.steps: List[AlgorithmStep] = steps
        self.response_step: AlgorithmStep = response_step


response_algo_steps_map: Dict[ResponseType, ProcessConfiguration] = {
    ResponseType.RESULT: ProcessConfiguration([GenerateFhirCNFStep(), ExecuteFhirQueriesStep(),
                                               ExtractFhirIdsStep(), ResolveCNFStep()], BuildXmlResponseStep()),
    ResponseType.INTERNAL: ProcessConfiguration([GenerateFhirCNFStep()], BuildInternalResponseStep())
}
"""
Dictionary that maps each implemented ResponseType to the List of steps that have to be executed on the Input
 to achieve the wished result
"""
