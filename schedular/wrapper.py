import json
import requests
from datetime import datetime
class Job:
    def __init__(self, job_id, job_name, cron_expression, last_run_time):
        self.job_id = job_id
        self.job_name = job_name
        self.cron_expression = cron_expression
        self.last_run_time = last_run_time

class JobsWrapper:

    def __init__(self):
        self._jobs = []

    def _get_jobs(self):

        response = requests.get('http://192.168.29.167:5000/jobs/last-runs')
        return response.json()
    
    def _deserialize_jobs(self):

        for job in self._get_jobs():
            self._jobs.append(Job(job['job_id'], job['job_name'], job['cron_expression'], datetime.strptime(job['last_run_time'], '%Y-%m-%d %H:%M:%S')))
        return self._jobs

    def get_jobs(self):
        return self._deserialize_jobs()

