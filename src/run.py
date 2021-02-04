import time
import timeit
from argparse import ArgumentParser, Namespace
from typing import List, Set, Optional
from xml.etree.ElementTree import Element

from algorithm import AlgorithmStep
from configuration.io_types import QuerySyntax
from configuration.parser_configuration import syntax_parser_map
from configuration.process_configuration import response_algo_steps_map
from fhir import generate_fhir_cnf, get_patient_ids_from_bundle, build_result_set_from_query_results, execute_fhir_query
from worker.communication import Instruction

__debug = True

# Arguments supplied by the user
args: Optional[Namespace] = None


def run(instruction: Instruction) -> List[str]:
    """
    Main function, runs the entire Script and returns a set of IDs

    :param instruction: The query which is to be executed against a FHIR Server
    :return: The resulting IDs that fit the query
    """
    algorithm: List[AlgorithmStep] = response_algo_steps_map[instruction.response_type]
    for step in algorithm:
        step.process(instruction)

    result_set = instruction.algo_step

    # fhir_cnf = prepare_fhir_cnf(instruction.request_data, instruction.query_syntax)
    # fhir_cnf_responses = execute_fhir_queries(fhir_cnf)
    # result_set = build_result_set(fhir_cnf_responses)

    print(f"\nresult_set_size:\n{len(result_set)}")
    print(f"result_set:\n{result_set}")
    return result_set


def build_result_set(fhir_cnf_responses: List[List[List[Element]]]) -> List[str]:
    """
    Builds the resulting set of IDs by resolving the CNF

    :param fhir_cnf_responses: List of Disjunctions, in turn made up of a List of query results, made up of pages
    :return: List of IDs that fit the original query definition
    """
    start_time = timeit.default_timer()
    fhir_query_results = extract_resulting_ids(fhir_cnf_responses)
    result_set = build_result_set_from_query_results(fhir_query_results)
    elapsed = timeit.default_timer() - start_time
    if __debug:
        print(f"Took {elapsed} seconds to analyse responses and build result_set")
    return result_set


def extract_resulting_ids(fhir_cnf_responses: List[List[List[Element]]]) -> List[List[List[Set[str]]]]:
    """
    Replaces the FHIR-Bundles with a set of contained IDs

    :param fhir_cnf_responses: FHIR-Responses in CNF format
    :return: IDs contained in the FHIR-Bundles
    """
    # TODO: Find a cleaner way to do this
    fhir_query_results = []
    for fhir_disjunction_response in fhir_cnf_responses:
        fhir_cnf_results = []
        for fhir_paged_responses in fhir_disjunction_response:
            page_ids = []
            for fhir_response in fhir_paged_responses:
                patient_ids = get_patient_ids_from_bundle(fhir_response)
                page_ids.append(patient_ids)
            fhir_cnf_results.append(page_ids)
        fhir_query_results.append(fhir_cnf_results)
    return fhir_query_results


def execute_fhir_queries(fhir_cnf: List[List[str]]) -> List[List[List[Element]]]:
    """
    executes the FHIR Queries

    :param fhir_cnf: FHIR Queries structured in a CNF form
    :return: The raw FHIR Responses made up of pages structured like the input queries
    """
    start_time = timeit.default_timer()
    fhir_cnf_responses = [[execute_fhir_query(query) for query in fhir_disjunction] for fhir_disjunction in
                          fhir_cnf]
    elapsed = timeit.default_timer() - start_time
    if __debug:
        print(f"Took {elapsed} seconds to execute fhir queries")
    return fhir_cnf_responses


def prepare_fhir_cnf(query_definition: str, query_syntax: QuerySyntax) -> List[List[str]]:
    """
    Parses the Query and for each panel generates a List of queries

    :param query_syntax: Syntax of the query to be processed
    :param query_definition: the untouched Query definition
    :return: List queries for each panel
    """

    intermediate_query_repr = syntax_parser_map[query_syntax](query_definition)
    fhir_cnf = generate_fhir_cnf(intermediate_query_repr)
    return fhir_cnf


if __name__ == "__main__":
    # Parse arguments
    parser = ArgumentParser(description="FLARE, run feasibility queries via standard HL7 FHIR search requests")
    parser.add_argument("query_file", type=str, help="path to the file containing the query")

    # TODO Implement the mapping option
    parser.add_argument("--mapping", type=str, help="path to the file containing the i2b2 to FHIR mappings")
    parser.add_argument("--syntax", type=str, choices=list(QuerySyntax),
                        help="detail which syntax the query is in, default is I2B2", default="I2B2")
    args = parser.parse_args()

    # Create instruction
    try:
        with open(args.query_file, 'r') as file:
            ins = Instruction(file.read(), "local_request", time.time_ns(), query_syntax=QuerySyntax[args.syntax])
    except IOError:
        print("Error reading the query file")

    # Run the Script
    run(ins)
