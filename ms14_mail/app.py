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


# Define a route for the homepage
@app.route('/') 
def home():
    log_this(request)
    return 'ms14_working XX = ' 


####################################################################################################
####################################################################################################
####################################################################################################


# Define a route for the homepage
@app.route('/send_mail', methods=["POST","GET"])
def login():
    log_this(request)
    data = {"email":"sent"}
    
    response = app.ms.requests.get("http://10.5.16.212:9022/offer_mail")
    custom_response = app.response_class(
            response=json.dumps(data),
            mimetype='application/json',
            status=200
        )
    return custom_response
# Run the app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9014)