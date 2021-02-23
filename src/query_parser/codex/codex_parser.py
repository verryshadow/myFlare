from typing import List

from jsonschema import validate
import json

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


def parse_codex_query_string(codex_json: str) -> List[List[dict]]:
    validate_codex_json(codex_json)
    codex = json.loads(codex_json)
    query = codex["query"]
    inclusion_criteria = query["inclusionCriteria"]
    for disjunction in inclusion_criteria:
        for inclusion_criterion in disjunction:
            print(inclusion_criterion)
    return codex


if __name__ == "__main__":
    with open("example.json", "r") as codex_json_file:
        cdx = parse_codex_query_string(codex_json_file.read())
        # print(cdx)

