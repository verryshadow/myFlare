import time
from flask import Flask, request
import xml.etree.ElementTree as ET
from run import run

app = Flask(__name__)


def build_response(result_set, i2b2_request):
    x_result_set = ET.Element("resultSet")
    x_result = ET.Element("result")
    x_result.attrib["value"] = str(len(result_set))
    x_result_set.insert(0, x_result)
    return x_result_set

#    for result in result_set:
#       x_result = ET.Element("result")
#       x_result.attrib["value"] = result
#       x_result_set.insert(0, x_result)


@app.route("/i2b2", methods=["POST"])
def handle_i2b2_query():
    # Execute and timestamp
    start_time = time.time()
    i2b2_request = request.data.decode("UTF-8")
    i2b2_query = request.data.decode("UTF-8")
    result_set = run(i2b2_query)
    response = build_response(result_set, i2b2_request)
    end_time = time.time()
    delta = end_time - start_time

    # Insert timestamps into result_set
    x_start_time = ET.Element("start_time")
    x_start_time.attrib["value"] = str(start_time)

    x_end_time = ET.Element("end_time")
    x_end_time.attrib["value"] = str(end_time)

    x_delta = ET.Element("delta")
    x_delta.attrib["value"] = str(delta)

    response.insert(0, x_end_time)
    response.insert(0, x_start_time)
    response.insert(0, x_delta)
    response = ET.tostring(response).decode("UTF-8")

    return str(response)
