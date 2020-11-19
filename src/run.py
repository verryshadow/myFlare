from typing import List, Set
from xml.etree.ElementTree import Element

from fhir import generate_fhir_cnf, get_patient_ids_from_bundle, build_result_set_from_query_results, execute_fhir_query
from i2b2.i2b2_parser import parse_i2b2_query_xml_string
import timeit

__debug = True


def run(i2b2_query_definition: str) -> List[str]:
    fhir_cnf = prepare_fhir_cnf(i2b2_query_definition)
    fhir_cnf_responses = execute_fhir_queries(fhir_cnf)
    result_set = build_result_set(fhir_cnf_responses)

    print(f"\nresult_set_size:\n{len(result_set)}")
    print(f"result_set:\n{result_set}")
    return result_set


def build_result_set(fhir_cnf_responses: List[List[List[Element]]]) -> List[str]:
    start_time = timeit.default_timer()
    fhir_query_results = extract_resulting_ids(fhir_cnf_responses)
    result_set = build_result_set_from_query_results(fhir_query_results)
    elapsed = timeit.default_timer() - start_time
    if __debug:
        print(f"Took {elapsed} seconds to analyse responses and build result_set")
    return result_set


def extract_resulting_ids(fhir_cnf_responses: List[List[List[Element]]]) -> List[List[List[Set[str]]]]:
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
    start_time = timeit.default_timer()
    fhir_cnf_responses = [[execute_fhir_query(query) for query in fhir_disjunction] for fhir_disjunction in
                          fhir_cnf]
    elapsed = timeit.default_timer() - start_time
    if __debug:
        print(f"Took {elapsed} seconds to execute fhir queries")
    return fhir_cnf_responses


def prepare_fhir_cnf(i2b2_query_definition: str) -> List[List[str]]:
    start_time = timeit.default_timer()
    parsed_i2b2 = parse_i2b2_query_xml_string(i2b2_query_definition)
    if __debug:
        print(f"Parsed i2b2:\n {parsed_i2b2}\n")
    fhir_cnf = generate_fhir_cnf(parsed_i2b2)
    if __debug:
        print(f"generated FHIR_cnf:\n {fhir_cnf}\n")
    elapsed = timeit.default_timer() - start_time
    if __debug:
        print(f"Took {elapsed} seconds to evaluate i2b2 and generate FHIR queries")
    return fhir_cnf


if __name__ == "__main__":
    with open('I2B2/i2b2_demo.xml', 'r') as file:
        run(file.read())
