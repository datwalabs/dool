from flask import Flask, Response
import Services.LogStreamService as StreamLogs
# services
import Services.UserService as UserService
import Services.EnvironmentService as EnvService
import Services.JobService as JobService
import Services.OperatorService as OperatorService
from flask_cors import CORS,cross_origin

app = Flask(__name__)
CORS(app,resources={r"/*": {"origins": "http://localhost:3000"}})
# Basic route for the homepage
@app.route('/')
def home():
    return UserService.hello()

# User Management
@app.route('/users', methods=['POST'])
def create_user():
    UserService.create_user(None)
    return '', 201

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


@app.route('/log-stream')
@cross_origin()  # Allows all domains; adjust as needed
def log_stream():
    return Response(StreamLogs.read_log_file(), mimetype='text/event-stream')

if __name__ == '__main__':
    # Run the app on localhost (127.0.0.1) with debug mode on
    # app.run(debug=True, host='192.168.29.167')
    app.run(debug=True, threaded=True)
