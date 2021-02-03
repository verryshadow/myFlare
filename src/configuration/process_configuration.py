from typing import Dict, List

from configuration.io_types import ResponseType
from algorithm import AlgorithmStep
from algorithm.steps import ParseStep


response_algo_steps_map: Dict[ResponseType, List[AlgorithmStep]] = {
    ResponseType.RESULT: [],
    ResponseType.INTERNAL: [ParseStep()]
}
"""
Dictionary that maps each implemented ResponseType to the List of steps that have to be executed on the Input
 to achieve the wished result
"""
