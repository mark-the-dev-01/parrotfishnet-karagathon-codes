from collections import OrderedDict
from google.cloud import firestore
from flask import Flask, request
import json
from datetime import datetime
import decimal
import logging

app = Flask(__name__)
db = firestore.Client()
entries_ref = db.collection('entries')
fishermen_ref = db.collection('fishermen')
results = []
fisherman_list = []


@app.route("/")
def root():
    return "Hello from the server side"


@app.route("/dashboard/api/addmapdata", methods=["POST"])
def add_map_data():
    result = False

    if request.files:
        mapdata = request.files["mapdata"]
        data = json.loads(mapdata.stream.read())
        for d in data:
            entries_ref.add(d)
        result = True

    val = {'result': result}
    response = app.response_class(
        response=json.dumps(val),
        status=200,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/dashboard/api/allfishermen/<version>")
@app.route("/dashboard/api/allfishermen")
def all_fishermen(version=0.3):
    global fisherman_list
    updateResults = False

    if (len(fisherman_list) == 0):
        updateResults = True
    else:
        if (fisherman_list[0]['version'] != version):
            fisherman_list = []
            updateResults = True

    if (updateResults):
        query = fishermen_ref.where("version", "==", version).stream()
        for q in query:
            try:
                res = {}
                res['id'] = q.id
                res.update(q.to_dict())
                fisherman_list.append(res)

            except Exception as error:
                logging.exception(error)

    response = app.response_class(
        response=json.dumps(fisherman_list),
        status=200,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@app.route("/dashboard/api/alldata/<version>")
@app.route("/dashboard/api/alldata")
def all_data(version=0.5):
    global results
    updateResults = False

    if (len(results) == 0):
        updateResults = True
    else:
        if (results[0]['version'] != version):
            results = []
            updateResults = True

    if (updateResults):
        query = entries_ref.where("version", "==", version).stream()
        for q in query:
            try:
                res = {}
                res['id'] = q.id
                res.update(q.to_dict())
                res['date_added_str'] = datetime.fromtimestamp(
                    res['date_added']).strftime("%m/%d/%Y %H:%M:%S")
                res['telemetry']['date_proc_str'] = datetime.fromtimestamp(
                    res['telemetry']['date_proc']).strftime("%m/%d/%Y %H:%M:%S")
                results.append(res)

            except Exception as error:
                logging.exception(error)

    response = app.response_class(
        response=json.dumps(results),
        status=200,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


@ app.route("/dashboard/api/get/<devicename>")
def get_device_data(devicename):
    deviceData = []
    if (len(results) > 0):
        for res in results:
            try:
                if (res['device']['name'] == devicename):
                    deviceData.append(res)
            except Exception as error:
                logging.exception(error)

    data = json.dumps(deviceData)

    response = app.response_class(
        response=data,
        status=200,
        mimetype='application/json'
    )
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
