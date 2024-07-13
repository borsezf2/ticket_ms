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
    return 'ms50_working XX = ' 


####################################################################################################
####################################################################################################
####################################################################################################


@app.route('/register', methods=["POST","GET"])
def register():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9000/register")
    return "User registered as Dolly chai wala"

@app.route('/login', methods=["POST","GET"])
def login():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9001/login")
    return "Login successfull for Dolly chai wala"

@app.route('/login_2', methods=["POST","GET"])
def login_2():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9001/login_2")
    return "Login 2 successfull for Dolly chai wala"

@app.route('/search_train', methods=["POST","GET"])
def search_train():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9002/search_train")
    return "KGP gareeb rath : price 6969 : Thursday"

@app.route('/book_train', methods=["POST","GET"])
def book_train():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9003/book_train")
    return "KGP gareeb rath is booked ;)"

@app.route('/search_ticket', methods=["POST","GET"])
def search_ticket():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9004/search_ticket")
    return "Ticket for KGP gareeb rath"

@app.route('/ticket_pdf', methods=["POST","GET"])
def ticket_pdf():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9004/ticket_pdf")
    return "PDF ticket for KGP gareeb rath"

@app.route('/cancel_ticket', methods=["POST","GET"])
def cancel_ticket():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9005/cancel_ticket")
    return "KGP gareeb rath ticket canceled : Sad :("

@app.route('/add_train', methods=["POST","GET"])
def add_train():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9015/add_train")
    return "New train: KGP Ameer rath is added"

@app.route('/update_train', methods=["POST","GET"])
def update_train():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9017/update_train")
    return "KGP gareeb rath is updated"

@app.route('/add_ads', methods=["POST","GET"])
def add_ads():
    log_this(request)
    response = app.ms.requests.get("http://10.5.16.212:9019/add_ads")
    return "New ads added"

# Run the app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9050)