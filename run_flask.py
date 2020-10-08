import time
from flask import Flask, request
import xml.etree.ElementTree as ET
from run import run

app = Flask(__name__)


@app.route("/i2b2", methods=["POST"])
def handle_i2b2_query():
    # Execute and timestamp
    start_time = time.time()
    i2b2_query = request.data.decode("UTF-8")
    result_set = run(i2b2_query, xml=True)
    end_time = time.time()
    delta = end_time - start_time

    # Insert timestamps into result_set
    x_start_time = ET.Element("start_time")
    x_start_time.attrib["value"] = str(start_time)

    x_end_time = ET.Element("end_time")
    x_end_time.attrib["value"] = str(end_time)

    x_delta = ET.Element("delta")
    x_delta.attrib["value"] = str(delta)

    result_set.insert(0, x_end_time)
    result_set.insert(0, x_start_time)
    result_set.insert(0, x_delta)
    result_set = ET.tostring(result_set).decode("UTF-8")

    return str(result_set)
