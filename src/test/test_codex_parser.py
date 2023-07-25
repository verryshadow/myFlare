#run from codex-flare/src
from os import close
import unittest
import json

from query_parser.codex.codex_parser import parse_codex_query_string
from query_parser.codex.codex_parser import curate_codex_json


class TestCurateCodexJson(unittest.TestCase):
    def test_curator(self):
        print("Starting Curation Test!")
        testCaseGT_file = open("test/level_one_queries/testCaseGT.json")
        testCaseGT_data = json.load(testCaseGT_file)
        testCaseGT_string = json.dumps(testCaseGT_data)
        #testCaseGT_string = testCaseGT_string.replace('"', "'")

        testCase_file = open("test/level_one_queries/testCase.json")
        testCase_data = json.load(testCase_file)
        testCase_string = json.dumps(testCase_data)
        
        out = curate_codex_json(testCase_string)
        #print(out)
        self.maxDiff=None
        message = "Curation did not work! Check single vs double quotes in json.dumps"
        '''
        print(out)
        print(testCaseGT_string)
        print(type(out))
        print(type(testCaseGT_string))
        '''
        self.assertEqual(out, testCaseGT_string, message)
        print("Curation Test finished!")

        testCase_file.close()
        testCaseGT_file.close()

'''
class TestParseCodexQueryString(unittest.TestCase):
    print("Start Level 1 Testing!")

    def test_json_query(self):
        with open("test/level_one_queries/testCaseGT.json", "r") as test_file:
            test = json.load(test_file)
            print(test)
            test_string = json.dumps(test)
            out = parse_codex_query_string(test_string)
            print(out)


    print("Level 1 Testing finished!")
    pass
'''