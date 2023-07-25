from typing import List, Optional
import itertools

from jsonschema import validate
import json

# with open("schema.json", "r") as schema_file:
with open("query_parser/codex/schema.json", "r") as schema_file:
    schema = json.load(schema_file)

with open("query_parser/codex/codex-code-tree.json", "r") as ontology_file:
    ontology = json.load(ontology_file)

codex_mapping = {}


def load_codex_mapping():
    with open("query_parser/codex/codex-term-code-mapping.json", "r") as mapping_file:
        codex_mapping_input = json.load(mapping_file)

        for mapping in codex_mapping_input:
            codex_mapping[get_hash_from_term_code(mapping['key'])] = mapping


def get_hash_from_term_code(term_code):
    if 'code' in term_code:
        hash_val = {
            'code': term_code['code'],
            'system': term_code['system'],
        }
    else:
        hash_val = {
            'code': term_code[0]['code'],
            'system': term_code[0]['system'],
        }

    return hash(frozenset(hash_val.items()))


def flatten_tree(tree: dict, code_string: list):
    if 'children' in tree:
        for child in tree['children']:
            if 'termCodes' in child and child['termCodes']['code'] is not None:

                code_string = code_string + [f'{child["termCodes"]["system"]}|{child["termCodes"]["code"]}']

            code_string = flatten_tree(child, code_string)

    return code_string


def get_subtree_for_code(tree: dict, search_string: str):
    found_tree = None

    if 'children' in tree:

        for child in tree['children']:
            if 'termCodes' in child:
                if search_string == child['termCodes']['code']:
                    return child

            if found_tree is None:
                found_tree = get_subtree_for_code(child, search_string)

    return found_tree


def get_codes_for_code(code, system):
    sub_tree = get_subtree_for_code(ontology, code)

    if sub_tree is None:
        return 

    flattened_subtree = flatten_tree(sub_tree, [])

    if flattened_subtree == '':
        return [f'{system}|{code}']

    return [f'{system}|{code}'] + flattened_subtree

def validate_codex_json(codex: str) -> None:
    """
    Validates a json string according to the codex structured query schema

    :param codex: Codex structured query in json syntax
    :raises:
        ValidationError: Error describing how the given json was invalid
    """
    validate(instance=json.loads(codex), schema=schema)


def parse_codex_query_string(codex_json: str) -> List[List[List[dict]]]:
    validate_codex_json(codex_json)

    codex = json.loads(codex_json)

    src_inclusion_criteria = codex["inclusionCriteria"]
    query = []
    inclusion_criteria = []
    for src_disjunction in src_inclusion_criteria:
        disjunction = []
        for src_criterion in src_disjunction:
            fhir_search_criteria = parse_criterion(src_criterion)
            disjunction = disjunction + fhir_search_criteria
        inclusion_criteria.append(disjunction)
    query.append(inclusion_criteria)

    if "exclusionCriteria" in codex:
        src_exclusion_criteria = codex["exclusionCriteria"]
    else:
        src_exclusion_criteria = []

    exclusion_criteria = []
    for src_disjunction in src_exclusion_criteria:
        disjunction = []
        temp_conjunction = []
        for src_criterion in src_disjunction:
            temp_conjunction.append(parse_criterion(src_criterion))

        criterion_disjunction = itertools.product(*temp_conjunction)

        for criterion_tuple in criterion_disjunction:
            exclusion_criteria.append(list(criterion_tuple))

    query.append(exclusion_criteria)

    return query


def parse_fixed_criteria(fixed_criteria: dict):
    fhir_fixed_string = ""

    for criterion in fixed_criteria:
        first_value = criterion['value'][0]['code']
        criterion_values = str(first_value)

        for value in criterion['value'][1:]:
            criterion_values += f',{value["code"]}'

        fhir_fixed_string += f'&{criterion["searchParameter"]}={criterion_values}'

    return fhir_fixed_string


def parse_value_filter(value_filter: dict, valueSearchParameter: str, first: bool):
    filter_type = value_filter["type"]
    fhir_filter_string = ""
    concat_string = "&"

    # FIXME: It would better to have a composite filter_type probably even composite quantity and concept
    if valueSearchParameter == "component-code-value-concept":
        fhir_filter_string += f'${value_filter["comparator"]}{str(value_filter["value"])}|{value_filter["unit"]["code"]}'
        return fhir_filter_string
    elif valueSearchParameter == "mii-provision-provision-code-type":
        first_concept = value_filter['selectedConcepts'][0]
        value_concepts = f'${first_concept["code"]}'
        for concept in value_filter['selectedConcepts'][1:]:
            value_concepts += f',{concept["code"]}'
        fhir_filter_string += value_concepts
        return fhir_filter_string

    if first:
        concat_string = "?"

    if filter_type == "quantity-comparator":
        fhir_filter_string += f'{concat_string}{valueSearchParameter}='
        if "unit" in value_filter:
            fhir_filter_string += f'{value_filter["comparator"]}{str(value_filter["value"])}|{value_filter["unit"]["code"]}'
        else:
            fhir_filter_string += f'{value_filter["comparator"]}{str(value_filter["value"])}'
        return fhir_filter_string
    elif filter_type == "quantity-range":
        fhir_filter_string += f'{concat_string}{valueSearchParameter}'
        fhir_filter_string += f'=ge {str(value_filter["minValue"])}|{value_filter["unit"]["code"]}'
        fhir_filter_string += "&" + valueSearchParameter
        fhir_filter_string += f'=le {str(value_filter["maxValue"])}|{value_filter["unit"]["code"]}'
        return fhir_filter_string
    elif filter_type == "concept":
        fhir_filter_string = f'{concat_string}{valueSearchParameter}='
        first_concept = value_filter['selectedConcepts'][0]
        value_concepts = f'{first_concept["system"]}|{first_concept["code"]}'

        for concept in value_filter['selectedConcepts'][1:]:
            value_concepts += f',{concept["code"]}'

        fhir_filter_string += value_concepts

        return fhir_filter_string
    else:
        raise ValueFilterNotFound(
            f"{filter_type} is not a recognized filter function")

    return ""


class ValueFilterNotFound(Exception):
    def __init__(self, message):
        super.__init__(message)

def parse_criterion(json_criterion) -> List[dict]:
    fhir_search_criterion = ""
    if not get_hash_from_term_code(json_criterion["termCodes"]) in codex_mapping:
        print("mapping missing for termCodes:", json_criterion["termCodes"])
        return fhir_search_criterion

    mapping = codex_mapping[get_hash_from_term_code(
        json_criterion["termCodes"])]

    fhir_search_criterion += f'{mapping["fhirResourceType"]}'

    fhir_search_criteria = []

    if "valueFilter" in json_criterion:
        if "termCodeSearchParameter" in mapping:
            # es wird immer das Element der Stelle 0 hergenommen, da es sich immer um 1 Array mit 1 Dictionary handelt. Das gilt sowohl für code, als auch für system
            fhir_search_criterion += f'?{mapping["termCodeSearchParameter"]}={json_criterion["termCodes"][0]["system"]}|{json_criterion["termCodes"][0]["code"]}'
            fhir_search_criterion += parse_value_filter(
                json_criterion['valueFilter'], mapping['valueSearchParameter'], False)
        else:
            fhir_search_criterion += parse_value_filter(
                json_criterion['valueFilter'], mapping['valueSearchParameter'], True)

        if "fixedCriteria" in mapping:
            fhir_search_criterion += parse_fixed_criteria(mapping['fixedCriteria'])

        fhir_search_criteria = fhir_search_criteria + [fhir_search_criterion]
    else:
        codes = [json_criterion["termCodes"][0].get("system")]
        for code in codes:
            fhir_search_criterion = f'{mapping["fhirResourceType"]}?{mapping["termCodeSearchParameter"]}' + \
                                    f'={code}'
            if "fixedCriteria" in mapping:
                fhir_search_criterion += parse_fixed_criteria(mapping['fixedCriteria'])

            fhir_search_criteria = fhir_search_criteria + [fhir_search_criterion]

    return fhir_search_criteria


def remove_empty_elements(d):
    """recursively remove empty lists, empty dicts, or None elements from a dictionary"""

    def empty(x):
        return x is None or x == {} or x == []

    if not isinstance(d, (dict, list)):
        return d
    elif isinstance(d, list):
        return [v for v in (remove_empty_elements(v) for v in d) if not empty(v)]
    else:
        return {k: v for k, v in ((k, remove_empty_elements(v)) for k, v in d.items()) if not empty(v)}


load_codex_mapping()

if __name__ == "__main__":
    with open("../example-queries/specimen-example.json", "r") as codex_json_file:
        cdx = parse_codex_query_string(codex_json_file.read())
        print(cdx)
