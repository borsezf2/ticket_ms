import json
from flask import Flask,request
import requests
from pyms.flask.app import Microservice


# Create a Flask app instance
ms = Microservice()
app = ms.create_app()

# app = Flask(__name__)

# Define a route for the homepage
@app.route('/') 
def home():
    val = str(app.ms)
    print("## val = ",val)
    return 'ms1_working fine' + val

# Define a route for the homepage
@app.route('/login', methods=["GET","POST"])
def login():
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
    data = {"user":"Harshzf2", "password":"123"}
    response = app.ms.requests.get("http://10.5.16.213:9014")
    return "response_data"


# Run the app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9001)