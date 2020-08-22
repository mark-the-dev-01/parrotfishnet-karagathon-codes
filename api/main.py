from google.cloud import firestore
from flask import Flask
import json
from datetime import datetime
from collections import OrderedDict

app = Flask(__name__)

db = firestore.Client()
entries_ref = db.collection('entries')
results = []


@app.route("/")
def root():
    return "Hello from the server side"


@app.route("/dashboard/api/alldata")
def all_data():
    allData = []
    if (len(results) == 0):
        query = entries_ref.stream()
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
                pass
            except Exception as error:
                pass

    allData = json.dumps(results)
    # resp = Flask.make_response(val, 200)
    # resp.headers['Access-Control-Allow-Origin'] = '*'

    response = app.response_class(
        response=allData,
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
                pass

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

# from flask import Flask
# from datetime import datetime
# import re
# import json

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import firestore

# from google.cloud import datastore

# import os

# app = Flask(__name__)

# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#     'projectId': 'marine-protected-areas-v279620',
# })
# db = firestore.client()
# entries_ref = db.collection('entries')
# results = []


# @app.route("/dashboard/api/alldata")
# def get_by_device():
#     val = {}

#     if (len(results) == 0):
#         query = entries_ref.stream()
#         for q in query:
#             try:
#                 res = {}
#                 res['id'] = q.id
#                 res.update(q.to_dict())
#                 res['date_added_str'] = datetime.fromtimestamp(
#                     res['date_added']).strftime("%m/%d/%Y %H:%M:%S")
#                 res['telemetry']['date_proc_str'] = datetime.fromtimestamp(
#                     res['telemetry']['date_proc']).strftime("%m/%d/%Y %H:%M:%S")
#                 results.append(res)
#             except Exception as error:
#                 pass

#     val = json.dumps(results)
#     # resp = Flask.make_response(val, 200)
#     # resp.headers['Access-Control-Allow-Origin'] = '*'

#     response = app.response_class(
#         response=val,
#         status=200,
#         mimetype='application/json'
#     )
#     response.headers['Access-Control-Allow-Origin'] = '*'
#     return response


# @ app.route("/dashboard/api/get/<devicename>")
# def get_device_data(devicename):
#     val = []
#     if (len(results) > 0):
#         for res in results:
#             try:
#                 if (res['device']['name'] == devicename):
#                     val.append(res)
#             except Exception as error:
#                 pass

#     return json.dumps(val)


# @ app.route("/")
# def home():
#     return "Hello, Flask!"


# @ app.route("/dashboard/api/hello/<name>")
# def hello_there(name):
#     now = datetime.now()
#     formatted_now = now.strftime("%A, %d %B, %Y at %X")

#     # Filter the name argument to letters only using regular expressions. URL arguments
#     # can contain arbitrary text, so we restrict to safe characters only.
#     match_object = re.match("[a-zA-Z]+", name)

#     if match_object:
#         clean_name = match_object.group(0)
#     else:
#         clean_name = "Friend"

#     content = "Hello there, " + clean_name + "! It's " + formatted_now
#     return content
