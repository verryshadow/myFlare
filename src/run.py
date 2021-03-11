import time
from argparse import ArgumentParser, Namespace
from typing import List, Optional
import sys

from algorithm import AlgorithmStep
from configuration.io_types import QuerySyntax, ResponseType
from configuration.parser_configuration import syntax_parser_map
from configuration.process_configuration import response_algo_steps_map
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import default_logger

__debug = True

# Arguments supplied by the user
args: Optional[Namespace] = None


def run(instruction: Instruction) -> str:
    """
    Main function, runs the entire Script and returns a set of IDs

    :param instruction: The query which is to be executed against a FHIR Server
    :return: The finished response string that can be transferred through http
    """

    logger = default_logger

    algorithm: List[AlgorithmStep] = response_algo_steps_map[instruction.response_type].steps
    parsed_input = parse_input(instruction)

    print(parsed_input, file=sys.stderr)

    processed_inclusion_criterions: List[List] = []
    for inclusion_criterion in parsed_input:
        for step in algorithm:
            inclusion_criterion = step.process(instruction, inclusion_criterion, logger)
        processed_inclusion_criterions.append(inclusion_criterion)

    if instruction.response_type is not ResponseType.INTERNAL and len(processed_inclusion_criterions) > 1:
        result_set = set(processed_inclusion_criterions[0])
        excluded_set = set.intersection(*[set(processed_inclusion_criterion) for processed_inclusion_criterion in
                                          processed_inclusion_criterions[1:]])
        result_set -= set(excluded_set)
        result_set = list(result_set)
    else:
        result_set = processed_inclusion_criterions[0]
    response = response_algo_steps_map[instruction.response_type].response_step.process(instruction, result_set, logger)
    logger.result(response)
    return response


def parse_input(instruction: Instruction) -> List[List[List[dict]]]:
    instruction.state = ExecutionState.PARSING
    default_logger.log_progress_event(instruction, information=instruction.query_syntax.name)

    intermediate_query_repr: List[List[List[dict]]] = \
        syntax_parser_map[instruction.query_syntax](instruction.request_data)

    return intermediate_query_repr


if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser(description="FLARE, run feasibility queries via standard HL7 FHIR search requests")
    parser.add_argument("query_file", type=str, help="path to the file containing the query")

    # TODO Implement the mapping option
    parser.add_argument("--mapping", type=str, help="path to the file containing the i2b2 to FHIR mappings")
    parser.add_argument("--querySyntax", type=str, choices=[e.name for e in QuerySyntax],
                        help="detail which syntax the query is in, default is I2B2", default="I2B2",
                        dest="query_syntax")
    parser.add_argument("--responseType", type=str, choices=[e.name for e in ResponseType], default="RESULT",
                        help="detail what result the user wants to process, default is result", dest="response_type")
    args = parser.parse_args()

    # Create instruction
    try:
        with open(args.query_file, 'r') as file:
            ins = Instruction(file.read(), "local_request", time.time_ns(), query_syntax=QuerySyntax[args.query_syntax],
                              response_type=ResponseType[args.response_type])
    except IOError:
        print("Error reading the query file")
        exit(-1)

    # Run the Script
    run(ins)
