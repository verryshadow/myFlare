from typing import List

import xml.etree.ElementTree as ET

import requests
from requests.auth import HTTPBasicAuth
import urllib3
urllib3.disable_warnings()

# TODO: Create parallel requests with user config, maybe slower?
def execute_queries(queries: List[str]) -> List[ET.Element]:
    ret = []
    for query in queries:
        print(f"Query:{query}")
        response = requests.get(query, verify=False) #, auth=HTTPBasicAuth('fhiruser', 'change-password'))
        print(f"Respone: {response.text}")
        x_response = ET.fromstring(response.text)
        ret.append(x_response)
    return ret
