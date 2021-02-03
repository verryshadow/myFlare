from enum import Enum

from query_parser.codex.codex_parser import parse_codex_query_string
from query_parser.i2b2.i2b2_parser import parse_i2b2_query_xml_string

QuerySyntax = Enum("QuerySyntax", "CODEX I2B2")
"""
An enum of all allowed syntaxes that a query can be in
"""

syntax_parser_map: dict = {QuerySyntax.CODEX: parse_codex_query_string,
                           QuerySyntax.I2B2: parse_i2b2_query_xml_string}
"""
Dictionary that maps each allowed query syntax to it's query_parser function
"""


def content_type_to_query_syntax(content_type: str) -> QuerySyntax:
    """
    For a given Content-Type header

    :param content_type: string given in the header, values being e.g. codex/json or i2b2/xml
    :return: enum representing the input format
    """
    # Get first part of media-type in uppercase, split of charset, boundary and
    content_type = content_type.split(";")[0].split("/")[0].upper()
    return QuerySyntax[content_type]
