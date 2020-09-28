# parse xml file
from FHIR.fhir_executor import execute_queries
from FHIR.fhir_parser import get_patient_ids_from_bundle, build_result_set_from_query_results
from FHIR.fhir_query_gen import generate_fhir_cnf
from I2B2.i2b2_parser import parse_i2b2_query_xml_string
import xml.etree.ElementTree as ET

with open('I2B2/i2b2_example.xml', 'r') as file:
    parsed_i2b2 = parse_i2b2_query_xml_string(file.read())
    print(parsed_i2b2)

fhir_cnf = generate_fhir_cnf(parsed_i2b2)
print(fhir_cnf)

fhir_cnf_responses = [execute_queries(fhir_disjunction) for fhir_disjunction in fhir_cnf]

# Write to file for debugging purposes
count = 0
for fhir_disjunction_response in fhir_cnf_responses:
    for fhir_response in fhir_disjunction_response:
        with open(f'FHIR/fhir_responses/{count}.xml', 'w') as out:
            out.write(ET.tostring(fhir_response).decode('utf-8'))
        count += 1

fhir_query_results = []
for fhir_disjunction_response in fhir_cnf_responses:
    fhir_cnf_results = []
    for fhir_response in fhir_disjunction_response:
        patient_ids = get_patient_ids_from_bundle(fhir_response)
        print(patient_ids)
        fhir_cnf_results.append(patient_ids)
    fhir_query_results.append(fhir_cnf_results)

result_set = build_result_set_from_query_results(fhir_query_results)
print(len(result_set))
print(result_set)
