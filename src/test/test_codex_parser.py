#import nose2
import unittest

from query_parser.codex.codex_parser import load_codex_mapping, get_hash_from_term_code, flatten_tree, get_subtree_for_code, validate_codex_json, parse_codex_query_string, parse_fixed_criteria, parse_value_filter, parse_criterion


class TestLoadCodexMapping(unittest.TestCase):
    def test_test(self):
        print("This is a Tests")
        # Key in Mapping
        #self.assertRaises(KeyError, load_codex_mapping, )

class TestGetHashFromTermCode(unittest.TestCase):
    def test_term_code(self):
        pass

class TestFlattenTree(unittest.TestCase):
    pass

class TestGetSubtreeForCode(unittest.TestCase):
    pass

class TestGetCodesForCode(unittest.TestCase):
    pass

class TestValidateCodexJson(unittest.TestCase):
    pass

class TestParseCodexQueryString(unittest.TestCase):
    pass

class TestParseFixedCriteria(unittest.TestCase):
    pass

class TestParseValueFilter(unittest.TestCase):
    pass

class TestParseCriterion(unittest.TestCase):
    pass


