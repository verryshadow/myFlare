import csv
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

        path = "test/testCases_copy"
        extension = "json"

        testCase_content_list = []
        instructionSet = []
        response_list = []
        with open("test/testResults" + '.csv', 'w', newline='') as f:
            sheet = csv.writer(f)
            for filename in os.listdir(path):
                if filename.endswith(extension):
                    with open(os.path.join(path, filename)) as f:
                        # testCase_content_list.append(f.read().decode("iso-8859-1"))
                        query_input = f.read()
                        # query_input = query_input.decode("iso-8859-1")
                        testCase_content_list.append(query_input)

                        queue_insertion_time: int = time.time_ns()
                        uuid: UUID = uuid4()

                        singleInstruction = Instruction(query_input, str(uuid), queue_insertion_time,
                                                        query_syntax=query_syntax, response_type=response_type)
                        instructionSet.append(singleInstruction)

                        try:
                            result = run_codex_query(singleInstruction)
                            if result != "1":
                                test_name = filename
                                test_name.strip(".json")
                                query_json = json.loads(query_input)
                                for inclusionCriteria in query_json["inclusionCriteria"][0]:
                                    sheet.writerow([test_name, inclusionCriteria["termCode"]["system"],
                                                    inclusionCriteria["termCode"]["code"]])
                                response_list.append(result)

                        except TypeError:
                            query_json = json.loads(query_input)
                            for inclusionCriteria in query_json["inclusionCriteria"][0]:
                                sheet.writerow([test_name, inclusionCriteria["termCode"]["system"],
                                                inclusionCriteria["termCode"]["code"]])
                            print(query_input)
                            print("This one")

        pass

    print("Finshed Query Sync Test!")
