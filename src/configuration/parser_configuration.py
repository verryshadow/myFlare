from typing import Dict, Callable, List

from configuration.io_types import QuerySyntax
from query_parser.codex.codex_parser import parse_codex_query_string
from query_parser.i2b2.i2b2_parser import parse_i2b2_query_xml_string


syntax_parser_map: Dict[QuerySyntax, Callable[[str], List[List[Dict]]]] = {
    QuerySyntax.CODEX: parse_codex_query_string,
    QuerySyntax.I2B2: parse_i2b2_query_xml_string
}
"""
Dictionary that maps each allowed query syntax to it's query_parser function
"""
