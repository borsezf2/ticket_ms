import json
import string
from flask import Flask, request, jsonify, Response
import requests
from pyms.flask.app import Microservice
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pymysql
from opentracing.propagation import Format
from opentracing.ext import tags
import opentracing

from jaeger_client import Config

from pymongo import MongoClient
import os
import random
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
    app.logger.info("\nTrace_LOG_START:,TS={} \n{}".format(ts,request.headers))
    logger.info("LOG_START_wsgi ,TS={}".format(ts))
    logger.info("headers = \n{}".format(request.headers))
    pid_str = str(getpid())
    tid_str = str(threading.get_native_id())
    logger.info("PID = \n{}".format(pid_str))
    logger.info("TID = \n{}".format(tid_str))

# MySQL Configuration
app.config['MYSQL_HOST'] = 'user_db'
# app.config['MYSQL_HOST'] = '10.5.16.215'
app.config['MYSQL_USER'] = 'sql_user'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'user_db'



# Connect to the MySQL database
conn = pymysql.connect(
    host='user_db',
    user='sql_user',
    password='password',
    database='user_db'
)


# Initialize MySQL
# mysql = MySQL(app)
# print("## MYSQL = ",str(mysql))

# Define a route for the homepage
@app.route('/')
def home():
    return 'ms6_working'

# Define a route for the homepage
@app.route('/login', methods=['POST'])
def login():
    log_this(request)
    post_data = json.loads(request.data)
    data = {"key":"logged in!!"}
    # r = app.ms.requests.get("http://10.5.16.212:9006",data=json.dumps(data))
    # print("## r = ",r)
    
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute("SELECT * FROM users where email = \"{}\" and password = \"{}\" ".format("Harsh@example.com","1234"))
    # Fetch the result
    result = cursor.fetchall()

    if len(result)==1:
        r = app.ms.requests.get("http://10.5.16.213:9014")
        custom_response = app.response_class(
                response=json.dumps({"msg":1}),
                mimetype='application/json',
                status=200
            )
    else:
        custom_response = app.response_class(
                response=json.dumps({"msg":0}),
                mimetype='application/json',
                status=200
            )
    return custom_response

@app.route('/login_2', methods=['GET'])
def login2():
    log_this(request)
    data = {"key":"logged in!!"}
    # r = app.ms.requests.get("http://10.5.16.212:9006",data=json.dumps(data))
    # print("## r = ",r)
    r = app.ms.requests.get("http://10.5.16.213:9014")

    custom_response = Response(json.dumps(data), status=200, content_type='application/json')    
    custom_response = app.response_class(
            response=json.dumps(data),
            mimetype='application/json',
            status=200
        )
    return custom_response


@app.route('/sql_test', methods=['GET'])
def sql_test():
    log_this(request)
    try:
        
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Create the users table if it doesn't exist
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(50) NOT NULL,
                email VARCHAR(100) NOT NULL,
                password VARCHAR(50)
            )
        ''')

        # Insert some data into the table
        users_data = [
            ('Borse', 'Harsh@example.com','1234'),
            ('Jane Smith', 'jane@example.com','1234'),
            ('Bob Johnson', 'bob@example.com','1234')
        ]
        cursor.executemany('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', users_data)

        # Commit changes and close the connection
        conn.commit()
        # conn.close()

        return "SQL WORKED"
    except Exception as e:
        return f"Error: {str(e)}"


def insertSQL():

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Create the users table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(50) NOT NULL,
            email VARCHAR(100) NOT NULL,
            password VARCHAR(50)
        )
    ''')

    # Insert some data into the table
    users_data = [
        ('Borse', 'Harsh@example.com','1234'),
        ('Jane Smith', 'jane@example.com','1234'),
        ('Bob Johnson', 'bob@example.com','1234')
    ]
    cursor.executemany('INSERT INTO users (name, email, password) VALUES (%s, %s, %s)', users_data)

    # Commit changes and close the connection
    conn.commit()    



# Initialize Jaeger tracer
tracer = opentracing.Tracer()



@app.route('/sql_test2', methods=['GET'])
def sql_test2():
    log_this(request)
    app.logger.info("There are my headers: \n{}".format(request.headers))
    app.logger.info("tracer: \n{}".format(tracer))

    # try:
        # Start a new span for the MySQL query
    with tracer.start_active_span('mysql_query') as scope:
        span = scope.span
        span.set_tag(tags.SPAN_KIND, tags.SPAN_KIND_RPC_CLIENT)
        span.set_tag(tags.DATABASE_INSTANCE, 'sql')
        span.set_tag(tags.DATABASE_STATEMENT, 'CREATE TABLE users ...')  # Example MySQL statement
        # Inject span context into headers
        headers = {}
        tracer.inject(span.context, Format.HTTP_HEADERS, headers)
        temp = tracer.extract(Format.HTTP_HEADERS, headers)
        
        # Execute the MySQL query with tracing
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(50) NOT NULL, email VARCHAR(100) NOT NULL)')
        users_data = [('Harsh Borse', 'Harsh@example.com'), ('Jane Smith', 'jane@example.com'), ('Bob Johnson', 'bob@example.com')]
        cursor.executemany('INSERT INTO users (name, email) VALUES (%s, %s)', users_data)
        conn.commit()
        
        # Close cursor
        cursor.close()

    return "SQL 2 WORKED = " + str(temp)
    # except Exception as e:
    #     return f"Error: {str(e)}"



# Define MongoDB connection parameters
mongo_host = "mongo"
mongo_port = 27017
mongo_db = "mydatabase"

# Connect to MongoDB
client = MongoClient(host=mongo_host, port=mongo_port)
db = client[mongo_db]

# Route to get data from MongoDB
@app.route('/mongo_data')
def get_data():
    log_this(request)
    data = db["user_db"].find_one()  # Change 'collection_name' to your collection name
    return str(data)



# Function to generate random data
def generate_random_data():
    return {
        'name': ''.join(random.choices(string.ascii_letters, k=10)),
        'age': random.randint(18, 60),
        'city': ''.join(random.choices(string.ascii_letters, k=8))
    }



# Insert random data into MongoDB
def insert_data(num_records):
    collection = db["user_db"] # Change 'collection_name' to your collection name
    for _ in range(num_records):
        data = generate_random_data()
        collection.insert_one(data)


# Route to get data from MongoDB
@app.route('/mongo_in')
def set_data():
    log_this(request)
    insert_data(10) # Change 'collection_name' to your collection name
    return "DONE"



# Run the app
if __name__ == '__main__':
    insertSQL()
    app.run(debug=True,host="0.0.0.0",port=9006)