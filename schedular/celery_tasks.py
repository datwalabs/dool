from celery import Celery, chain, group
from celery.utils.log import get_task_logger
from collections import deque
from operators.PythonOperator.PythonOperator import PythonOperator
from wrapper import Task  # Ensure Task is imported

app = Celery('jobs', 
             broker='redis://localhost:6379/0',
             backend='redis://localhost:6379/1')

# Configure Celery
# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],
#     result_serializer='json',
#     timezone='UTC',
#     enable_utc=True,
#     worker_pool='prefork',
#     worker_concurrency=8,
#     worker_prefetch_multiplier=1,
#     worker_max_tasks_per_child=200,
#     worker_autoscaler='celery.worker.autoscale:Autoscaler',
#     worker_autoscale_min=2,
#     worker_autoscale_max=8,
# )

logger = get_task_logger(__name__)

@app.task(name='schedular.celery_tasks.execute_step',bind=True)
def execute_step(self,step,**kwargs):
    print('Executing Step')
    if step["operator"]['operator_slug'] == 'python3':
        return PythonOperator(filepath=fr"{step['task_params']}").execute()
    return None

def create_workflow(job):
    workflow = []
    tasks = job.tasks
    group_tasks = []
    while len(tasks) > 0:
        temp_list = []
        while True:
            t = tasks.pop(0)
            temp_list.append(t.to_dict())  # Convert Task to dict
            if len(tasks) > 0:
                if tasks[0].sequence != t.sequence:
                    group_tasks = group(execute_step.si(s) for s in temp_list)
                    workflow.append(group_tasks)  # Append the last group_task
                    temp_list = []
                    break
            else:
                group_tasks = group(execute_step.si(s) for s in temp_list)
                workflow.append(group_tasks)  # Append the last group_task
                break
    print(len(workflow))
    print(len(group_tasks))
    print('Workflow Created')
    return chain(*workflow)

def execute_job(job):
    workflow = create_workflow(job)
    print('Applying Async')
    result = workflow.apply_async()
    return result
