import json
import requests
from datetime import datetime
from operators.PythonOperator.PythonOperator import PythonOperator

class Operator:
    def __init__(self, operator_id, operator_name, operator_slug):
        self.operator_id = operator_id
        self.operator_name = operator_name
        self.operator_slug = operator_slug

    def to_dict(self):
        return {
            "operator_id": self.operator_id,
            "operator_name": self.operator_name,
            "operator_slug": self.operator_slug
        }

class Task:
    def __init__(self, task_id, task_name, task_params, sequence,operator):
        self.task_id = task_id
        self.task_name = task_name
        self.operator = operator
        self.task_params = task_params
        self.sequence = sequence
    
    def to_dict(self):
           return {
               'task_id': self.task_id,
               'task_name': self.task_name,
               'task_params': self.task_params,
               'sequence': self.sequence,
               'operator': self.operator.to_dict() if self.operator else None
           }
    

class Job:
    def __init__(self, job_id=None, job_name=None, cron_expression=None, last_run_time=None,tasks=[]):
        self.job_id = job_id
        self.job_name = job_name
        self.cron_expression = cron_expression
        self.last_run_time = last_run_time
        self.tasks = tasks
    
    def _deserialize_job(self):
        response = self._get_job()
        self.job_id = response['job_id']
        self.job_name = response['job_name']
        self.cron_expression = response['cron']
        self.last_run_time = response['last_run']
        self.is_active = response['is_active']
        self.last_run = response['last_run']
        for task in response['tasks']:
            operatorObj = Operator(task['operator']['operator_id'], task['operator']['operator_name'], task['operator']['operator_slug'])    
            taskObj = Task(task['task_id'], task['task_name'], task['task_params'], task['sequence'],operator=operatorObj)
            self.tasks.append(taskObj)
            print(task['task_params'])
            print(taskObj.task_params)
        return self._sort_tasks()
    
    def _sort_tasks(self):
        self.tasks.sort(key=lambda x: x.sequence)
        return self

    def _get_job(self):

        response = requests.get(f'http://192.168.29.167:5000/job/{self.job_id}')
        return response.json()

    def get_job(self):
        return self._deserialize_job()

class JobRuns:

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
