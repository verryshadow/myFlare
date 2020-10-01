from flask import Flask, request
from run import run

app = Flask(__name__)


@app.route("/i2b2", methods=["POST"])
def handle_i2b2_query():
    i2b2_query = request.data.decode("UTF-8")
    result_set = run(i2b2_query)
    return str(result_set)
