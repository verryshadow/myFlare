import os
from typing import List

fhir_format = "_format=xml"


def generate_fhir_cnf(i2b2_query: List[List[dict]]) -> List[List[str]]:
    cnf = [generate_fhir_disjunction(i2b2_panel) for i2b2_panel in i2b2_query]
    return cnf


def get_param(item: dict) -> str:
    return item["param"]


def get_code_and_sys(item: dict) -> str:
    code_and_sys = ""
    if item["sys"] != "":
        code_and_sys = f'{code_and_sys}{item["sys"]}|'
    if item["code"] != "":
        code_and_sys = f'{code_and_sys}{item["code"]}'
    return code_and_sys


def get_value_operator(item: dict) -> str:
    if "value_operator" in item:
        return item["value_operator"].lower()
    else:
        return ""


def get_value_search_param(value_type: str) -> str:
    if value_type == "NUMBER":
        return "value-quantity"


def generate_fhir_disjunction(panel: List[dict]) -> List[str]:
    """
    Generates a list of FHIR-queries from a list of dicts describing an i2b2 Panel

    :param panel: List of dictionaries describing i2b2 items
    :return: FHIR-queries corresponding to
    """
    queries = [generate_fhir_query(item) for item in panel]
    return queries


def generate_fhir_query(item: dict) -> str:
    """
    Generates a single FHIR-query from a dict describing an i2b2 item

    :param item: dictionary describing an i2b2 item
    :return: Corresponding query url
    """
    query = f'{item["res"]}?{get_param(item)}={get_code_and_sys(item)}'
    if 'constrain_by_value' in item:
        # TODO: Handle value_unit_of_measure and other value_types than NUMBER
        query = f'{query}&{get_value_search_param(item["constrain"]["value_type"])}=' \
                f'{get_value_operator(item["constrain"])}{item["constrain"]["value_constraint"]}'
    query = f'{query}&{fhir_format}'
    return query
