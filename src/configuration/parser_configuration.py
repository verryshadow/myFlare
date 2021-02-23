from typing import Dict, Callable, List
import json

from configuration.io_types import QuerySyntax
from query_parser.codex.codex_parser import parse_codex_query_string
from query_parser.i2b2.i2b2_parser import parse_i2b2_query_xml_string


syntax_parser_map: Dict[QuerySyntax, Callable[[str], List[List[Dict]]]] = {
    QuerySyntax.CODEX: parse_codex_query_string,
    QuerySyntax.I2B2: parse_i2b2_query_xml_string,
    # Internal syntax is given, just parse json and leave as is
    QuerySyntax.INTERNAL: lambda x: json.loads(x)
}
"""
Dictionary that maps each allowed query syntax to it's query_parser function
"""
