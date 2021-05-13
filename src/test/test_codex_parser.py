#run from codex-flare/src
from os import close
import unittest
import json

from query_parser.codex.codex_parser import parse_codex_query_string
from query_parser.codex.codex_parser import curate_codex_json


class TestCurateCodexJson(unittest.TestCase):
    print("Testing code proposal")

    def test_curator(self):
        testCaseGT_file = open("test/level_one_queries/testCaseGT.json")
        testCaseGT_data = json.load(testCaseGT_file)
        #print(testCaseGT_data)
        
        
        testCase_file = open("test/level_one_queries/testCase.json")
        testCase_data = json.load(testCase_file)
        print(testCase_data)
        
        inclusionData = testCase_data['inclusionCriteria']
        print(inclusionData)
        
        testCase_data.pop("inclusionCriteria")
        print(testCase_data)


        out = curate_codex_json(testCase_data)
        #print(out)

        #with open("test/level_one_queries/testCase.json", "r") as test_file:
         #       test = json.load(test_file)
         #       out = curate_codex_json(test_file.read())
          #      print(out)
                #self.assertEqual(test_file.read(), testCasteGTJSON.read())
                #print(test["inclusionCriteria"])

        testCase_file.close()
        testCaseGT_file.close()

'''
class TestParseCodexQueryString(unittest.TestCase):
    print("Level 1 Testing")

    def test_json_query(self):
        with open("test/level_one_queries/testRef.json", "r") as test_file:
            test = json.load(test_file)
            #print(test)



    pass
'''