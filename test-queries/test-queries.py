import requests
import json
import os

for filename in os.listdir("."):
    if filename.endswith('.json'):
        with open(filename) as json_file:
            print("Run test: ", filename)

            expected_number = int(filename.split('.')[0][-1:])
            data = json.load(json_file)
            url = "http://localhost:5000/query-sync"
            headers = {'Content-Type': 'codex/json', 'Accept': 'internal/json'}

            res = requests.post(url, headers=headers, data=json.dumps(data))
            found_patients = res.json()
          
            print("Expected number of patients = ", expected_number, " Found number of patients = ", found_patients)
            assert(expected_number == found_patients)
