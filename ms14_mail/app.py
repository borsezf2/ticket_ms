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
    return 'ms14_working XX = ' 

# Define a route for the homepage
@app.route('/send_mail', methods=["POST","GET"])
def login():
    data = {"email":"sent"}
    custom_response = app.response_class(
            response=json.dumps(data),
            mimetype='application/json',
            status=200
        )
    return custom_response
# Run the app
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port=9014)