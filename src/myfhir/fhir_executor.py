import xml.etree.ElementTree as Etree
from typing import List, Tuple, Optional

import requests
import urllib3
import os
from requests import Response
from urllib.parse import urlparse
from urllib.parse import urlunparse
from urllib.parse import parse_qsl

from fhir.fhir_query_gen import fhir_format
from fhir.namespace import ns

from urllib.parse import urlparse

urllib3.disable_warnings()
server_base_url = os.environ.get("FHIR_BASE_URL") or "http://localhost:8081/fhir"
server_user = os.environ.get("FHIR_USER") or ""
server_pw = os.environ.get("FHIR_PW") or ""


def change_server_base_url(server_num):
    server_dict = {
        "1": "http://localhost:8081/fhir",
        "2": "http://localhost:8082/fhir",
        "3": "http://localhost:8083/fhir"
    }
    global server_base_url
    server_base_url = server_dict[server_num]
    print(server_base_url)
    return None

def get_server_base_url():
    print(server_base_url)
    return server_base_url

# TODO: Create parallel requests with user config.
#  Check whether this may slow down the process due to FHIR-server performance beforehand
def execute_fhir_query(query: str) -> List[Etree.Element]:
    """
    Executes a FHIR query, fetches all pages

    :param query: query to be executed 
    :return: List of FHIR-bundles in xml format returned by the FHIR server
    """
    ret = []
    print(server_base_url)
    next_query = f'{server_base_url}/{query}'
    init = True

    # Execute queries as long as there is a next page
    while next_query is not None:
        next_query, x_response = _execute_single_query(next_query.replace(" ", ""), init)
        # persist_query_response(x_response)
        ret.append(x_response)
        init = False
        # TODO die unteren 3 Zeilen löschen, ansonsten glaubt man, dass die Patienten von dem gleichen Server kommen, obwohl eigentlich der 2. Server abgefragt wird.
        # next_query = f'{"http://localhost:8082/fhir"}/{query}'
        # next_query, x_response = _execute_single_query(next_query.replace(" ", ""), init)
        # ret.append(x_response)

    return ret


def _execute_single_query(paged_query_url: str, init) -> Tuple[Optional[str], Etree.Element]:
    """
    Executes a single FHIR query and attempts to extract the URL to the next page

    :param paged_query_url: URL to be queried
    :raises RequestUnsuccessfulError: raised when response code is not 200
    :return: URL to the next page if the response contains one and the response to the given query
    """

    auth = None

    if server_user != '':
        auth = (server_user, server_pw)

    parsed_url = urlparse(paged_query_url)

    new_q = parsed_url._replace(path=parsed_url.path, query='')
    headers = {'Accept': 'application/fhir+xml', 'Prefer': 'handling=strict'}

    if init:
        new_q = parsed_url._replace(path=parsed_url.path + "/_search", query='')
        params = dict(parse_qsl(parsed_url.query))
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print(new_q)
        print(urlunparse(new_q))
        print(params)
        print(headers)
        print(auth)
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
        response = requests.post(urlunparse(new_q), data=params, headers=headers, auth=auth)
        print(response)
        print("the end")
    else:
        response = requests.get(paged_query_url, headers=headers, auth=auth)

    if response.status_code != 200:
        raise RequestUnsuccessfulError(response, f"failed request on url: {paged_query_url}")
    x_response = Etree.fromstring(response.text)
    return get_next_page_url(x_response), x_response


def get_next_page_url(x_response: Etree.Element) -> Optional[str]:
    """
    Fetch URL to the next page from a given response

    :param x_response: response potentially containing a relation tag with value next
    :return: URL to the next page
    """
    x_next = x_response.find("./ns0:link/ns0:relation[@value='next']/../ns0:url", ns)
    if x_next is not None:
        url = x_next.attrib["value"]
        return url
    return None


class RequestUnsuccessfulError(Exception):
    def __init__(self, response: Response, message: str):
        """
        :param response: Response to the unsuccessful request
        :param message: Message to be passed to the handler
        """
        self.response: Response = response
        """
        Response to the unsuccessful request
        """
        self.status_code: int = response.status_code
        """
        HTTP status code returned on failure
        """
        self.response_text: str = response.text
        """
        Response message given by the server
        """
        self.message: str = message
        """
        Message describing the exception
        """


persistence_index = 0


def persist_query_response(x_response):
    """
    For debugging purposes only, persists a query response under a running index

    :param x_response: response to be persisted
    """
    global persistence_index
    with open(f"../FHIR/fhir_responses/{persistence_index}.xml", "w", encoding="UTF-8") as persistence_file:
        persistence_file.writelines(Etree.tostring(x_response).decode("UTF-8"))
    persistence_index = persistence_index + 1
