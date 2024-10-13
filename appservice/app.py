from flask import Flask, Response, request
import Services.LogStreamService as StreamLogs

import json

# services
import Services.UserService as UserService
import Services.EnvironmentService as EnvService
import Services.JobService as JobService
import Services.OperatorService as OperatorService
from flask_cors import CORS, cross_origin

from Models.UserModels import *

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "http://localhost:5173"}})
# Basic route for the homepage
@app.route('/')
def home():
    return UserService.hello()

# User Management
@app.route('/users', methods=['POST'])
def create_user():
    userrequest = request.json
    user = CreateUserRequest(userrequest["username"], userrequest["email"], userrequest["password"])
    UserService.create_user(user)
    return '', 201

@app.route('/login', methods=['POST'])
def login_user():
    userrequest = request.json
    loginCredentials = LoginRequest(userrequest["username"], userrequest["password"])
    userinfo = UserService.login_user(loginCredentials)
    print("User Info", userinfo)
    return '', 200

@app.route('/users')
def get_users():
    return UserService.hello()

# Environment Management
@app.route('/environment', methods=['POST'])
def create_environment():
    EnvService.create_environment(None)
    return '', 201

# Jobs Management
@app.route('/jobs', methods=['POST'])
def create_job():
    jobjson = request.json
    result = JobService.create_job(jobjson)
    print(type(result))
    return json.dumps(result.to_dict()), 201

@app.route('/jobs/tasks', methods=['POST'])
def update_task():
    jobjson = request.json
    result = JobService.update_task(jobjson)
    print(type(result))
    return json.dumps(result.to_dict()), 201

@app.route('/jobs')
def get_all_jobs():
    return json.dumps(JobService.get_all_jobs())

@app.route('/job/<int:id>')
def get_job(id):
    data = JobService.get_job_by_id(id)
    return json.dumps(data), 200

# Operators
@app.route('/operators')
def get_operators():
    return OperatorService.get_operators()

# Runs
@app.route('/jobs/<int:id>/runs')
def get_all_job_runs(id):
    return JobService.jobs_runs(id)

@app.route('/jobs/<int:id>/running')
def get_job_runnig(id):
    return JobService.jobs_running(id)

@app.route('/jobs/last-runs')
def get_last_runs():
    return JobService.get_last_runs()


@app.route('/log-stream')
@cross_origin()  # Allows all domains; adjust as needed
def log_stream():
    return Response(StreamLogs.read_log_file(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) with debug mode on
    app.run(debug=True, host='192.168.29.167')
    # app.run(debug=True, threaded=True)
