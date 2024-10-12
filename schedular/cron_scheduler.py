import time
from datetime import datetime
from croniter import croniter
from wrapper import JobsWrapper

class CronScheduler:
    def __init__(self, jobs_wrapper):
        self.jobs_wrapper = jobs_wrapper

    def should_run(self, job, current_time):
        if job.last_run_time is None:
            return True
        cron = croniter(job.cron_expression, job.last_run_time)
        next_run = cron.get_next(datetime)
        return current_time >= next_run

    def execute_job(self, expression):
        print(f"Executing job for expression: {expression} at {datetime.now()}")
        # Replace this with your heavy data engineering job
        time.sleep(5)  # Simulating a long-running job
        print(f"Job completed for expression: {expression} at {datetime.now()}")

    def run(self):
        while True:
            current_time = datetime.now()
            for job in self.jobs_wrapper.get_jobs():
                if self.should_run(job, current_time):
                    self.execute_job(job.cron_expression)
            time.sleep(60)  # Check every minute

if __name__ == "__main__":
    jobs = JobsWrapper()
    scheduler = CronScheduler(jobs)
    scheduler.run()
