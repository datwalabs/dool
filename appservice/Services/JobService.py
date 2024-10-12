from datetime import *

def jobs_running():
    return "Jobs running"

def jobs_runs():
    return "Jobs runs"

def update_task(joob):
    pass

def create_job(job):
    pass

def get_last_runs():
    jobs = []
    intervals = [1,2,3,4,5,6]
    for i in range(1, 6 + 1):
        job = {
            'job_id': str(i),
            'job_name': f'job_{i}',
            'cron_expression': f'*/{intervals[i-1]} * * * *',
            'last_run_time': (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d %H:%M:%S')
        }
        jobs.append(job)
    return jobs