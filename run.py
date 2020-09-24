# parse xml file
from FHIR.fhir_executor import execute_queries
from FHIR.fhir_parser import get_patient_ids_from_bundle
from FHIR.fhir_query_gen import generate_fhir_cnf
from I2B2.i2b2_parser import parse_i2b2_query_xml_string
import xml.etree.ElementTree as ET

with open('I2B2/i2b2_example.xml', 'r') as file:
    parsed_i2b2 = parse_i2b2_query_xml_string(file.read())
    print(parsed_i2b2)

fhir_cnf = generate_fhir_cnf(parsed_i2b2)
print(fhir_cnf)

fhir_cnf_responses = [execute_queries(fhir_disjunction) for fhir_disjunction in fhir_cnf]
count = 0
for fhir_disjunction_response in fhir_cnf_responses:
    for fhir_response in fhir_disjunction_response:
        patient_ids = get_patient_ids_from_bundle(fhir_response)
        print(patient_ids)
        with open(f'FHIR/fhir_responses/{count}.xml', 'w') as out:
            out.write(ET.tostring(fhir_response).decode('utf-8'))
        count += 1

