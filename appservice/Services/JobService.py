import datetime
from datetime import *
from Models.JobModels import *
import Repositories.JobRepository as _repo

def jobs_running(job_id: int):
    return _repo.get_running_jobs_by_job_id(job_id)

def jobs_runs(job_id: int):
    return _repo.get_all_job_run_histories_by_job_id(job_id)

def update_task(data):
    tasks = []
    
    for task_data in data.get('tasks', []):
        
        task = TaskRequest(
            task_name=task_data.get('task_name'),
            operatorId=task_data.get('operator_id'),
            sequence=task_data.get('sequence'),
            task_params=task_data.get('task_params')
        )
        tasks.append(task)

    job = JobRequest(
        job_id=data.get('job_id'),
        job_name=data.get('job_name'),
        cron=data.get('cron'),
        is_active=data.get('is_active'),
        environment=data.get('environment'),
        tasks=tasks
    )
    result = _repo.update_job(job)
    return result

def create_job(data):
    tasks = []
    
    for task_data in data.get('tasks', []):
        
        task = TaskRequest(
            task_name=task_data.get('task_name'),
            operatorId=task_data.get('operator_id'),
            sequence=task_data.get('sequence'),
            task_params=task_data.get('task_params')
        )
        tasks.append(task)

    job = JobRequest(
        job_name=data.get('job_name'),
        cron=data.get('cron'),
        is_active=data.get('is_active'),
        environment=data.get('environment'),
        tasks=tasks
    )
    result = _repo.create_job(job)
    return result
    
def get_all_jobs():
    return _repo.get_all_jobs()

def get_job_by_id(id: int):
    return _repo.get_job_by_id(id)

def get_last_runs():
    jobs = [
        {
            'job_id': "55",
            'job_name': 'job_55',
            'cron_expression': '*/1 * * * *',
            'last_run_time': (datetime.datetime.now() - timedelta(seconds=90)).strftime('%Y-%m-%d %H:%M:%S')
        }
    ]
    # intervals = [1,2,3,4,5,6]
    # for i in range(1, 6 + 1):
    #     job = {
    #         'job_id': str(i),
    #         'job_name': f'job_{i}',
    #         'cron_expression': f'*/{intervals[i-1]} * * * *',
    #         'last_run_time': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
    #     }
    #     jobs.append(job)
    return jobs