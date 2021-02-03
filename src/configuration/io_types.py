from enum import Enum

QuerySyntax = Enum("QuerySyntax", "CODEX I2B2")
"""
An enum of all allowed syntaxes that a query can be in
"""

ResponseType = Enum("ResponseType", "RESULT INTERNAL")
"""
An enum of all supported Response data types
"""
