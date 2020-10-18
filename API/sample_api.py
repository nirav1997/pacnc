import flask
from flask import request, jsonify
import sqlite3
import pandas as pd
from postgres import PostGres

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


def risk_function(last_cases):
    n = len(last_cases)
    wgt_diff_arr = []
    for i in range(len(last_cases)-1, -1, -1):
        if i > 0:
            case = last_cases[i]
            prev_case = last_cases[i-1]
            wgt_diff_arr = [(case-prev_case)*(i+1)/n] + wgt_diff_arr
    if sum(wgt_diff_arr) < 0:
        return abs(min(wgt_diff_arr, key=abs))/abs(sum(wgt_diff_arr))
    risk_val = sum(wgt_diff_arr)/(len(wgt_diff_arr)*max(wgt_diff_arr))
    return risk_val

def getResponse(zipcode):
    db = PostGres().connect_db()
    with db.connect() as conn:
        query = "SELECT date, time, cases, totalpop from nccoviddata where zipcode='{}' and Date > current_date - interval '7' day".format(zipcode)
        df = pd.read_sql_query(query, conn).dropna()
        df = df.sort_values(['date', 'time'])
        avg_total_pop = df['TotalPop'].mean()
        cases = df['Cases'].values
        response = {"cases": cases,
                    "AverageTotalPop": avg_total_pop}
    return response


@app.route('/api/v1/risk_analysis', methods=['GET'])
def api_filter():
    query_parameters = request.args
    locations = query_parameters.get('zipcode')
    zipcodes = locations.split(",")
    avg_cases = [0]*7
    for zipcode in zipcodes:
        zipcode_data = getResponse(zipcode)
        print(zipcode_data['cases'])
        for i, case in enumerate(zipcode_data['cases']):
            avg_cases[i] += case/len(zipcodes)
    risk = risk_function(avg_cases)
    response = {"Avg Cases": avg_cases, "risk": risk}
    return jsonify(response)

app.run()