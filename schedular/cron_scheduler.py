import time
from datetime import datetime
from croniter import croniter
from wrapper import JobsWrapper
from celery_tasks import execute_job

class CronScheduler:
    def __init__(self, jobs_wrapper):
        self.jobs_wrapper = jobs_wrapper

    def should_run(self, job, current_time):
        if job.last_run_time is None:
            return True
        cron = croniter(job.cron_expression, job.last_run_time)
        next_run = cron.get_next(datetime)
        return current_time >= next_run

    def execute_job(self, job):
        print(f"Submitting job for expression: {job.cron_expression} at {datetime.now()}")
        result = execute_job(job.id)
        print(f"Job submitted with Celery task id: {result.id}")
        job.last_run_time = datetime.now()

    def run(self):
        while True:
            current_time = datetime.now()
            for job in self.jobs_wrapper.get_jobs():
                if self.should_run(job, current_time):
                    self.execute_job(job)
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    jobs = JobsWrapper()
    scheduler = CronScheduler(jobs)
    scheduler.run()
