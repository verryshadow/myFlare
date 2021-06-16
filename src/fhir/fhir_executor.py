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


# TODO: Create parallel requests with user config.
#  Check whether this may slow down the process due to FHIR-server performance beforehand
def execute_fhir_query(query: str) -> List[Etree.Element]:
    """
    Executes a FHIR query, fetches all pages

    :param query: query to be executed
    :return: List of FHIR-bundles in xml format returned by the FHIR server
    """
    ret = []

    next_query = f'{server_base_url}/{query}&{fhir_format}'

    init = True

    # Execute queries as long as there is a next page
    while next_query is not None:
        next_query, x_response = _execute_single_query(next_query, init)
        # persist_query_response(x_response)
        ret.append(x_response)
        init = False

    return ret


def _execute_single_query(paged_query_url: str, init) -> Tuple[Optional[str], Etree.Element]:
    """
    Executes a single FHIR query and attempts to extract the URL to the next page

    :param paged_query_url: URL to be queried
    :raises RequestUnsuccessfulError: raised when response code is not 200
    :return: URL to the next page if the response contains one and the response to the given query
    """

    parsed_url = urlparse(paged_query_url)

    new_q = parsed_url._replace(path=parsed_url.path + "?_format=xml", query='')

    if init:
        new_q = parsed_url._replace(path=parsed_url.path + "/_search?_format=xml", query='')

    params = dict(parse_qsl(parsed_url.query))
    response = requests.post(urlunparse(new_q), data=params, verify=False)

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
        url = x_next.attrib["value"] + "&" + fhir_format
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
