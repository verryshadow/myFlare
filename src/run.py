import time
import json
from argparse import ArgumentParser, Namespace
from typing import List, Optional

from algorithm import AlgorithmStep
from configuration.io_types import QuerySyntax, ResponseType
from configuration.parser_configuration import syntax_parser_map
from configuration.process_configuration import response_algo_steps_map
from worker.communication import Instruction
from worker.communication.instruction import ExecutionState
from worker.communication.logging_callback import default_logger
from fhir import execute_fhir_query
from fhir import get_patient_ids_from_bundle


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
    processed_inclusion_criterions: List[List] = []

    # Process all parsed inclusions
    for inclusion_criterion in parsed_input:
        for step in algorithm:
            inclusion_criterion = step.process(
                instruction, inclusion_criterion, logger)
        processed_inclusion_criterions.append(inclusion_criterion)

    # subtract all inclusion results from the first inclusion if response type is numeric and multiple inclusions exist
    if instruction.response_type is not ResponseType.INTERNAL and len(processed_inclusion_criterions) > 1:
        # Initial inclusion result
        result_set = set(processed_inclusion_criterions[0])
        # Merge inclusion results generated from Exclusions
        excluded_set = set.intersection(*[set(processed_inclusion_criterion) for processed_inclusion_criterion in
                                          processed_inclusion_criterions[1:]])
        result_set -= set(excluded_set)
        result_set = list(result_set)
    else:
        result_set = processed_inclusion_criterions[0]

    # Build result from generated set
    response = response_algo_steps_map[instruction.response_type].response_step.process(
        instruction, result_set, logger)
    logger.result(response)
    return response


def parse_input(instruction: Instruction) -> List[List[List[dict]]]:
    instruction.state = ExecutionState.PARSING
    default_logger.log_progress_event(
        instruction, information=instruction.query_syntax.name)

    intermediate_query_repr: List[List[List[dict]]] = \
        syntax_parser_map[instruction.query_syntax](instruction.request_data)
    return intermediate_query_repr

def run_translate_query(instruction: Instruction) -> str:
    logger = default_logger 
    parsed_input = parse_input(instruction)

    return json.dumps(parsed_input)

def run_codex_query(instruction: Instruction) -> str:
    """
    Main function, runs the entire Script and returns a set of IDs

    :param instruction: The query which is to be executed against a FHIR Server
    :return: The finished response string that can be transferred through http
    """
    logger = default_logger

    parsed_input = parse_input(instruction)

    # inclusion criteria
    fhir_cnf_responses = set()

    for fhir_disjunction in parsed_input[0]:
        fhir_disjunction_res = set()
        for query in fhir_disjunction:
            if query == "":
                continue
            paged_query_result = execute_fhir_query(query)
            for fhir_response in paged_query_result:
                pat_ids = get_patient_ids_from_bundle(fhir_response)
                fhir_disjunction_res = fhir_disjunction_res.union(pat_ids)

        if len(fhir_cnf_responses) == 0:
            fhir_cnf_responses = fhir_disjunction_res
        else:
            fhir_cnf_responses = fhir_cnf_responses.intersection(
                fhir_disjunction_res)

    # exclusion criteria
    fhir_dnf_responses = set()
    for fhir_conjunction in parsed_input[1]:
        fhir_conjunction_res = set()
        for query in fhir_conjunction:
            if query == "":
                continue

            paged_query_result = execute_fhir_query(query)

            pat_ids = set()
            for fhir_response in paged_query_result:
                pat_ids = pat_ids.union(
                    get_patient_ids_from_bundle(fhir_response))

            if len(fhir_conjunction_res) == 0:
                fhir_conjunction_res = pat_ids
            else:
                fhir_conjunction_res = fhir_conjunction_res.intersection(
                    pat_ids)

        fhir_dnf_responses = fhir_dnf_responses.union(fhir_conjunction_res)

    # subtract both sets from one another
    final_response = fhir_cnf_responses - fhir_dnf_responses

    return str(len(final_response))


if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser(
        description="FLARE, run feasibility queries via standard HL7 FHIR search requests")
    parser.add_argument("query_file", type=str,
                        help="path to the file containing the query")

    parser.add_argument("--mapping", type=str,
                        help="path to the file containing the i2b2 to FHIR mappings")
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
