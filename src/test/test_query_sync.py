import os
import unittest
import json
import time
from uuid import uuid4, UUID

from sys import exit

from flask.wrappers import Response


from run import run_codex_query
from run_server import content_type_to_query_syntax, accept_to_response_type
from worker.communication import Instruction


class TestRunCodexQuery(unittest.TestCase):
    print("Starting run_codex_query Test!")    


    def test_run_codex_query(self):

        content_type = "codex/json"
        query_syntax = content_type_to_query_syntax(content_type)
        accept = "internal/json"
        response_type = accept_to_response_type(accept)
        


        url = 'http://localhost:5000/query-sync'
        myobj = {
        "exclusionCriteria": [],
        "inclusionCriteria": [
          {
                "termCode": {
                    "code": "81839001",
                    "display": "",
                    "system": "http://snomed.info/sct"
                }
            },
            {
                "termCode": {
                    "code": "B01AB13",
                    "display": "",
                    "system": "http://fhir.de/CodeSystem/dimdi/atc"
                }
            }
        ],
        "version": ""
        }

        

        x = requests.post(url, data = myobj)















        path = "test/testCases_copy"
        extension = "json"

        testCase_content_list = []
        instructionSet = []
        response_list = []
        for filename in os.listdir(path):
            if filename.endswith(extension):
                with open(os.path.join(path, filename)) as f:
                    #testCase_content_list.append(f.read().decode("iso-8859-1"))
                    query_input = f.read()
                    #query_input = query_input.decode("iso-8859-1")
                    testCase_content_list.append(query_input)

                    queue_insertion_time: int = time.time_ns()
                    uuid: UUID = uuid4()

                    singleInstruction = Instruction(query_input, str(uuid), queue_insertion_time,
                                           query_syntax=query_syntax, response_type=response_type)
                    instructionSet.append(singleInstruction)

                    try:
                       response_list.append(run_codex_query(singleInstruction))
                       
                    except TypeError:
                        print(query_input)
                        print("This one")
                        exit()
                    
                            


        #print(testCase_content_list)
        #print(instructionSet)

        pass


    print("Finshed Query Sync Test!")