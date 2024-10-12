from celery import Celery, chain, group
from celery.utils.log import get_task_logger
import importlib

# Initialize Celery app
app = Celery('jobs', broker='pyamqp://guest@localhost//')

# Configure Celery to use RabbitMQ
app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

logger = get_task_logger(__name__)

@app.task
def execute_step(job_id, step_config):
    logger.info(f"Executing step for job {job_id}: {step_config['name']}")
    
    # Dynamically import the operator class
    module_name, class_name = step_config['operator'].rsplit('.', 1)
    module = importlib.import_module(module_name)
    operator_class = getattr(module, class_name)
    
    # Create an instance of the operator
    operator = operator_class(**step_config.get('params', {}))
    
    # Execute the operator
    result = operator.execute()
    
    logger.info(f"Step {step_config['name']} completed for job {job_id}")
    return result

def create_workflow(job_id, steps):
    workflow = []
    for step in steps:
        if isinstance(step, list):
            # If step is a list, create a group for parallel execution
            group_tasks = group(execute_step.s(job_id, s) for s in step)
            workflow.append(group_tasks)
        else:
            workflow.append(execute_step.s(job_id, step))
    
    return chain(*workflow)

def execute_job(job_id, steps):
    workflow = create_workflow(job_id, steps)
    result = workflow.apply_async()
    return result

if __name__ == '__main__':
    # For testing purposes
    test_steps = [
        {'name': 'Step 1', 'operator': 'operators.PythonOperator.PythonOperator', 'params': {'python_callable': lambda: print("Step 1")}},
        [
            {'name': 'Step 2a', 'operator': 'operators.PythonOperator.PythonOperator', 'params': {'python_callable': lambda: print("Step 2a")}},
            {'name': 'Step 2b', 'operator': 'operators.PythonOperator.PythonOperator', 'params': {'python_callable': lambda: print("Step 2b")}}
        ],
        {'name': 'Step 3', 'operator': 'operators.PythonOperator.PythonOperator', 'params': {'python_callable': lambda: print("Step 3")}},
        {'name': 'Step 4', 'operator': 'operators.PythonOperator.PythonOperator', 'params': {'python_callable': lambda: print("Step 4")}}
    ]
    job_result = execute_job('test_job_1', test_steps)
    print(f"Job submitted with id: {job_result.id}")