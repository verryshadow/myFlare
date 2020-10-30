from typing import List

import xml.etree.ElementTree as ET
from fhir.fhir_query_gen import fhir_format

import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings()


# TODO: Create parallel requests with user config, maybe slower?
def execute_query(query: str) -> List[ET.Element]:
    ret = []
    _ns = {"ns0": "http://hl7.org/fhir"}
    queries = [query]
    for query in queries:
        # print(f"Query:{query}")
        response = requests.get(query, verify=False)  # , auth=HTTPBasicAuth('fhiruser', 'change-password'))
        if response.status_code != 200:
            continue
        # print(f"Respone: {response.text}")
        x_response = ET.fromstring(response.text)
        x_next = x_response.find("./ns0:link/ns0:relation[@value='next']/../ns0:url", _ns)
        if x_next is not None:
            url = x_next.attrib["value"] + "&" + fhir_format
            if url is not None:
                queries.append(url)
        ret.append(x_response)
    return ret
