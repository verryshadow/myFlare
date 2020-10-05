# parse xml file
from typing import List

from FHIR.fhir_executor import execute_queries
from FHIR.fhir_parser import get_patient_ids_from_bundle, build_result_set_from_query_results
from FHIR.fhir_query_gen import generate_fhir_cnf
from I2B2.i2b2_parser import parse_i2b2_query_xml_string
import xml.etree.ElementTree as ET
import timeit
__debug = False


def run(i2b2_query_definition: str, xml=False):
    start_time = timeit.default_timer()
    parsed_i2b2 = parse_i2b2_query_xml_string(i2b2_query_definition)
    print(f"Parsed i2b2:\n {parsed_i2b2}\n")
    fhir_cnf = generate_fhir_cnf(parsed_i2b2)
    print(f"generated FHIR_cnf:\n {fhir_cnf}\n")
    elapsed = timeit.default_timer() - start_time
    print(f"Took {elapsed} seconds to evaluate i2b2 and generate FHIR queries")

    start_time = timeit.default_timer()
    fhir_cnf_responses = [execute_queries(fhir_disjunction) for fhir_disjunction in fhir_cnf]
    elapsed = timeit.default_timer() - start_time
    print(f"Took {elapsed} seconds to execute fhir queries")

    # Write to file for debugging purposes
    if __debug:
        count = 0
        for fhir_disjunction_response in fhir_cnf_responses:
            for fhir_response in fhir_disjunction_response:
                with open(f'FHIR/fhir_responses/{count}.xml', 'w') as out:
                    out.write(ET.tostring(fhir_response).decode('utf-8'))
                count += 1

        print("Query results")
        first_outer = True
        for fhir_disjunction_response in fhir_cnf_responses:
            if first_outer:
                first_outer = False
            else:
                print("and")
            first_inner = True
            for fhir_response in fhir_disjunction_response:
                if first_inner:
                    first_inner = False
                else:
                    print("or")
                print(f"{get_patient_ids_from_bundle(fhir_response)}")

    start_time = timeit.default_timer()
    fhir_query_results = []
    for fhir_disjunction_response in fhir_cnf_responses:
        fhir_cnf_results = []
        for fhir_response in fhir_disjunction_response:
            patient_ids = get_patient_ids_from_bundle(fhir_response)
            fhir_cnf_results.append(patient_ids)
        fhir_query_results.append(fhir_cnf_results)
    result_set = build_result_set_from_query_results(fhir_query_results)
    elapsed = timeit.default_timer() - start_time
    print(f"Took {elapsed} seconds to analyse responses and build result_set")

    print(f"\nresult_set_size:\n{len(result_set)}")
    print(f"result_set:\n{result_set}")
    if xml:
        x_result_set = ET.Element("resultSet")
        for result in result_set:
            x_result = ET.Element("result")
            x_result.attrib["value"] = result
            x_result_set.insert(0, x_result)
        result_set = x_result_set
    return ET.tostring(result_set).decode("UTF-8")


if __name__ == "__main__":
    with open('I2B2/i2b2_demo.xml', 'r') as file:
        run(file.read())
