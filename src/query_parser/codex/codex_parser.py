from typing import List, Optional

from jsonschema import validate
import json

# with open("schema.json", "r") as schema_file:
with open("query_parser/codex/schema.json", "r") as schema_file:
    schema = json.load(schema_file)

with open("query_parser/codex/codex-code-tree.json", "r") as ontology_file:
    ontology = json.load(ontology_file)

codex_mapping = {}

def load_codex_mapping():
    with open("query_parser/codex/codex-mapping.json", "r") as mapping_file:
        codex_mapping_input = json.load(mapping_file)
        
        for mapping in codex_mapping_input['entries']:
          codex_mapping[get_hash_from_term_code(mapping['key'])] = mapping


def get_hash_from_term_code(term_code):
    hash_val = {
      'code': term_code['code'],
      'system': term_code['system'],
    }

    return hash(frozenset(hash_val.items()))


def flatten_tree(tree: dict, code_string: str):
  
  if 'children' in tree:
    for child in tree['children']:
      if 'termCode' in child and child['termCode']['code'] is not None:

        if len(code_string) > 0:
          code_string = code_string + ","
        
        code_string = code_string + child['termCode']['code']
        
      code_string = flatten_tree(child, code_string)

  return code_string


def get_subtree_for_code(tree: dict, search_string: str):

  found_tree = None

  if 'children' in tree:

    for child in tree['children']:
      if 'termCode' in child:
        if search_string == child['termCode']['code']:
          return child

      if found_tree is None:
        found_tree = get_subtree_for_code(child, search_string)

  return found_tree


def get_codes_for_code(code):

  sub_tree = get_subtree_for_code(ontology, code)

  if sub_tree is None:
    return code

  flattened_subtree = flatten_tree(sub_tree , "")

  if flattened_subtree == '':
    return code

  return code + "," + flattened_subtree


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
            disjunction.append(parse_criterion(src_criterion))
        inclusion_criteria.append(disjunction)
    query.append(inclusion_criteria)

    if "exclusionCriteria" in codex:
        src_exclusion_criteria = codex["exclusionCriteria"]
    else:
        src_exclusion_criteria = []
    
    exclusion_criteria = []
    for src_disjunction in src_exclusion_criteria:
        disjunction = []
        for src_criterion in src_disjunction:
            disjunction.append(parse_criterion(src_criterion))
        exclusion_criteria.append(disjunction)
    query.append(exclusion_criteria)

    return query


def parse_fixed_criteria(fixed_criteria: dict):
    fhir_fixed_string = ""

    for criterion in fixed_criteria:
        
        first_value = criterion['value'][0]['code']
        criterion_values = str(first_value)

        for value in criterion['value'][1:]:
            criterion_values += "," + value['code']

        fhir_fixed_string += "&" + criterion['searchParameter'] + "=" + criterion_values


    return fhir_fixed_string 

def parse_value_filter(value_filter: dict, valueSearchParameter: str):
    filter_type = value_filter["type"]

    fhir_filter_string = ""

    # TODO: Implement Unit parsing
    if filter_type == "quantity-comparator":
        fhir_filter_string += "&" + valueSearchParameter + "=" + value_filter['comparator'] + str(value_filter['value'])
        return fhir_filter_string
    elif filter_type == "quantity-range":
        fhir_filter_string += "&" + valueSearchParameter + "=ge" + str(value_filter['minValue'])
        fhir_filter_string += "&" + valueSearchParameter + "=le" + str(value_filter['maxValue'])
        return fhir_filter_string
    elif filter_type == "concept":
        fhir_filter_string = "&" + valueSearchParameter + "="

        first_concept = value_filter['selectedConcepts'][0]

        #value_concepts = first_concept['system'] + "|" + first_concept['code']
        value_concepts = first_concept['code']

        for concept in value_filter['selectedConcepts'][1:]:
            
            ## TODO put concept system back in
            #value_concepts += "," + concept['system'] + "|" + concept['code'] 
            value_concepts += "," + concept['code']

        fhir_filter_string += value_concepts

        return fhir_filter_string
    else:
        raise ValueFilterNotFound(f"{filter_type} is not a recognized filter function")

    return ""


class ValueFilterNotFound(Exception):
    def __init__(self, message):
        super.__init__(message)


def parse_criterion(json_criterion) -> List[dict]:

    fhir_search_criterion = ""

    if not get_hash_from_term_code(json_criterion["termCode"]) in codex_mapping:
        print("mapping missing for termCode: " , json_criterion["termCode"])
        return fhir_search_criterion

    mapping = codex_mapping[get_hash_from_term_code(json_criterion["termCode"])]

    fhir_search_criterion += mapping['fhirResourceType'] + "?"
    
    if "valueFilter" in json_criterion:
        fhir_search_criterion += mapping['termCodeSearchParameter'] + "=" + json_criterion["termCode"]['code']
        fhir_search_criterion += parse_value_filter(json_criterion['valueFilter'], mapping['valueSearchParameter'])
    else:
      fhir_search_criterion += mapping['termCodeSearchParameter'] + "=" + get_codes_for_code(json_criterion["termCode"]['code'])

    if "fixedCriteria" in mapping:
        fhir_search_criterion += parse_fixed_criteria(mapping['fixedCriteria'])

    return fhir_search_criterion


load_codex_mapping()

if __name__ == "__main__":
    with open("query_parser/codex/example2.json", "r") as codex_json_file:
        cdx = parse_codex_query_string(codex_json_file.read())
        print(cdx)

