from typing import List, Optional

from jsonschema import validate
import json

# with open("schema.json", "r") as schema_file:
with open("query_parser/codex/schema.json", "r") as schema_file:
    schema = json.load(schema_file)


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
    src_query = codex["query"]

    src_inclusion_criteria = src_query["inclusionCriteria"]
    query = []
    inclusion_criteria = []
    for src_disjunction in src_inclusion_criteria:
        disjunction = []
        for src_criterion in src_disjunction:
            disjunction += parse_criterion(src_criterion)
        inclusion_criteria.append(disjunction)
    query.append(inclusion_criteria)

    src_exclusion_criteria = src_query["exclusionCriteria"]
    exclusion_criteria = []
    for src_disjunction in src_exclusion_criteria:
        disjunction = []
        for src_criterion in src_disjunction:
            disjunction.append(parse_criterion(src_criterion))
        exclusion_criteria.append(disjunction)
    query += exclusion_criteria

    return query


def parse_value_filter(value_filter: dict, criterion: dict):
    filter_type = value_filter["type"]
    clone_criterion = lambda: json.loads(json.dumps(criterion))
    criteria = []

    # TODO: Implement Unit parsing
    if filter_type == "quantity-comparator":
        constraint = {"value_operator": value_filter["comparator"], "value_constraint": value_filter["value"]}
        criterion["constrain"] = constraint
        criteria.append(criterion)
    elif filter_type == "quantity-range":
        min_crit = clone_criterion()
        max_crit = clone_criterion()
        max_crit["constrain"] = {"value_operator": "le", "value_constraint": value_filter["maxValue"]}
        min_crit["constrain"] = {"value_operator": "ge", "value_constraint": value_filter["minValue"]}
        criteria.append(max_crit)
        criteria.append(min_crit)
    elif filter_type == "concept":
        # TODO Implement
        pass
    else:
        raise ValueFilterNotFound(f"{filter_type} is not a recognized filter function")

    return criteria


class ValueFilterNotFound(Exception):
    def __init__(self, message):
        super.__init__(message)


def parse_criterion(json_criterion) -> List[dict]:
    term_code: dict = json_criterion["termCode"]
    value_filter: Optional[dict] = json_criterion["valueFilter"] if "valueFilter" in json_criterion else None

    resource: str = lookup_resource(term_code["code"])
    code = term_code["code"]
    code_system = term_code["system"]

    criterion = {"res": resource, "param": "code", "sys": code_system, "code": code}

    if value_filter is not None:
        criteria: List[dict] = parse_value_filter(value_filter, criterion)
    else:
        criteria = [criterion]

    return criteria


def lookup_resource(item_key: str) -> str:
    # TODO: Implement real lookup
    return "Observation"


if __name__ == "__main__":
    with open("example.json", "r") as codex_json_file:
        cdx = parse_codex_query_string(codex_json_file.read())
        # print(cdx)

