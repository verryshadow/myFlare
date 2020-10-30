import requests
import urllib3
from requests import ConnectionError
from requests.auth import HTTPBasicAuth
from IBM_transfer.common import endpoints, get_temp_file_path

urllib3.disable_warnings()
target_server_base_url = "http://localhost:5555/fhir/"


def build_target_url(endpoint: str, iD: str) -> str:
    return f'{target_server_base_url}{endpoint}/{iD}'


def read(obj_id: str, obj_type: str) -> str:
    with open(get_temp_file_path(obj_id, obj_type), 'r') as temp_file:
        text = temp_file.read()

    split = obj_id.split('-')
    # If ID like M-1004 is used, convert to numeric id and replace in the files
    if len(split) > 1:
        prefix = split[0]
        old_id = split[1]
        new_id = str(int(old_id) + (0 if prefix == 'O' else 10000))
        text.replace(obj_id, new_id)

    return text


for (endpoint, id_list) in endpoints.items():
    print(f'transfering endpoint {endpoint}')
    method = "POST" if endpoint=="Observation" else "PUT"
    for iD in id_list:
        # Post data
        target_url = build_target_url(endpoint,iD if method=="PUT" else "")
        try:
            response = requests.request(method, target_url, data=read(iD, endpoint), verify=False, auth=HTTPBasicAuth('fhiruser', 'change-password'),
                                     headers={"content-type": "application/fhir+xml"})
            if response.status_code not in range(200, 300):
                print(f'Failed to post id {iD} to endpoint {endpoint} with URL {target_url}, response:'
                      f' {response.status_code}: {response.content}')
                break
        except ConnectionError as e:
            print(f'Connection to target server failed: {e}')
            break
