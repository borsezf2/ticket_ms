import json
from flask import Flask,request
import requests
from pyms.flask.app import Microservice
import logging
import time
import subprocess
import threading
from os import getpid


logging.basicConfig(filename='tracing.log', level=logging.DEBUG)


# Create a Flask app instance
ms = Microservice()
app = ms.create_app()

# app = Flask(__name__)

logger = logging.getLogger('werkzeug') # grabs underlying WSGI logger
handler = logging.FileHandler('wsgi_logs.log') # creates handler for the log file
logger.addHandler(handler) # adds handler to the werkzeug WSGI logger

def log_this(request):
    ts = str(time.time())
    app.logger.info("\nTrace_LOG_START:,TS={}".format(ts))
    app.logger.info("\nheaders:,TS={}".format(ts,request.headers))
    # logger.info("LOG_START_wsgi ,TS={}".format(ts))
    # logger.info("headers = \n{}".format(request.headers))
    pid_str = str(getpid())
    tid_str = str(threading.get_native_id())
    # logger.info("PID = \n{}".format(pid_str))
    # logger.info("TID = \n{}".format(tid_str))
    app.logger.info("\nPID={}".format(pid_str))
    app.logger.info("\nTID={}".format(tid_str))
    print("## TEST PRINT ##")




# Define a route for the homepage
@app.route('/') 
def home():
    log_this(request)
    return 'ms1_working fine'

# Define a route for the homepage
@app.route('/login', methods=["GET","POST"])
def login():
    log_this(request)
    data = {"user":"Harshzf2", "password":"123"}
    try:
        file=open("login_log.log","w")
        file.write(json.dumps(data))
        file.close()
    except:
        pass

    response = app.ms.requests.post("http://10.5.16.215:9006/login",data=json.dumps(data))
    response_data = response.text
    return response_data
    response_data = json.loads(response_data)

    if response_data["msg"]==1:
        response_out = "Logged in"
    else:
        response_out = "fail"

    return response_out



@app.route('/login_2', methods=["GET","POST"])
def login3():
    log_this(request)
    data = {"user":"Harshzf2", "password":"123"}
    response = app.ms.requests.get("http://10.5.16.213:9014")
    return "response_data"


# Run the app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9001)