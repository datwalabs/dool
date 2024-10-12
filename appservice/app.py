from flask import Flask, request

# services
import Services.UserService as UserService
import Services.EnvironmentService as EnvService
import Services.JobService as JobService
import Services.OperatorService as OperatorService

from Models.UserModels import *

app = Flask(__name__)

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
    JobService.create_job(None)
    return '', 201

@app.route('/jobs/tasks', methods=['POST'])
def update_task():
    JobService.update_task(None)
    return '', 201

@app.route('/job/<int:id>')
def get_job(id):
    data = {
    "job_id": 12,
    "job_name": "UDM",
    "cron": "8 * * * *",
    "is_active": True,
    "environment": 1,
    "created_by": {
        "user_id": 12,
        "username": "paresh.sahoo"
    },
    "next_run": "2024-09-21T12:23:34",
    "created_at": "2024-09-21T12:23:34",
    "last_run": "2024-09-21T12:23:34",
    "success_runs": 12,
    "fail_runs": 4,
    "failed_last_10": 2,
    "running_now": True,
    "tasks": [
        {
        "task_id": "1",
        "task_name": "calculate_wh",
        "operator": {
            "operator_name": "python3",
            "operator_slug": "python3",
            "operator_id": 3
        },
        "sequence": 1,
        "task_params": "main.py --model CALCULATW_WH"
        },
        {
        "task_id": "2",
        "task_name": "calculate_wh",
        "operator": {
            "operator_name": "python3",
            "operator_slug": "python3",
            "operator_id": 3
        },
        "sequence": 2,
        "task_params": "main.py --model DECALC"
        },
        {
        "task_id": "3",
        "task_name": "calculate_wh",
        "operator": {
            "operator_name": "python3",
            "operator_slug": "python3",
            "operator_id": 3
        },
        "sequence": 2,
        "task_params": "main.py --model DECALC"
        },
        {
        "task_id": "4",
        "task_name": "calculate_wh",
        "operator": {
            "operator_name": "python3",
            "operator_slug": "python3",
            "operator_id": 3
        },
        "sequence": 3,
        "task_params": "main.py --model DECALC"
        },
        {
        "task_id": "5",
        "task_name": "calculate_wh",
        "operator": {
            "operator_name": "python3",
            "operator_slug": "python3",
            "operator_id": 3
        },
        "sequence": 4,
        "task_params": "main.py --model DECALC"
        }
    ]
    }
    return data, 200

# Operators
@app.route('/operators')
def get_operators():
    return OperatorService.get_operators()

# Runs
@app.route('/jobs/runs')
def get_all_job_runs():
    return JobService.jobs_runs()

@app.route('/jobs/running')
def get_job_runnig():
    return JobService.jobs_running()

@app.route('/jobs/last-runs')
def get_last_runs():
    return JobService.get_last_runs()

if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) with debug mode on
    app.run(debug=True, host='192.168.29.167')
