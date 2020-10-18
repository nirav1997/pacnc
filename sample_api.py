import flask
from flask import request, jsonify
import sqlite3
app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''




@app.route('/api/v1/risk_analysis', methods=['GET'])
def api_filter():
    query_parameters = request.args

    locations = query_parameters.get('zipcode')
    zipcodes = locations.split(",")
    print(zipcodes)
    
    risk_values={}
    
    return jsonify(risk_values)

app.run()