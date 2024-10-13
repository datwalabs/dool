import datetime

class JobRunHistory:
    def __init__(self, run_id: int, status: str, started_at: datetime.datetime, finished_at: datetime.datetime, logfile: str, logfile_id: int):
        self.run_id = run_id
        self.status = status
        self.started_at = started_at
        self.finished_at = finished_at
        self.logfile = logfile
        self.logfile_id = logfile_id

    def __repr__(self):
        return (f"JobRunHistory(run_id={self.run_id}, status='{self.status}', "
                f"started_at={self.started_at}, finished_at={self.finished_at}, "
                f"logfile='{self.logfile}', logfile_id={self.logfile_id})")

    def to_dict(self):
        return {
            'run_id': self.run_id,
            'status': self.status,
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'finished_at': self.finished_at.isoformat() if self.finished_at else None,
            'logfile': self.logfile,
            'logfile_id': self.logfile_id
        }

class Operator:
    def __init__(self, operator_name: str, operator_slug: str, operator_id: int, description: str):
        self.operator_name = operator_name
        self.operator_slug = operator_slug
        self.operator_id = operator_id
        self.description = description

    def __repr__(self):
        return f"Operator(operator_name={self.operator_name}, operator_slug={self.operator_slug}, operator_id={self.operator_id})"

    def to_dict(self):
        return {
            'operator_id': self.operator_id,
            'operator_name': self.operator_name,
            'operator_slug': self.operator_slug,
            'description': self.description
        }

class TaskRequest:
    def __init__(self, task_name: str, operatorId: Operator, sequence: int, task_params: str, task_id:int = 0, operator: Operator = None):
        self.task_name = task_name
        self.operatorId = operatorId
        self.sequence = sequence
        self.task_params = task_params
        self.task_id = task_id
        self.operator = operator

    def __repr__(self):
        return f"Task(task_name={self.task_name}, operator={self.operator}, sequence={self.sequence}, task_params={self.task_params})"

    def to_dict(self):
        return {
            'task_id': self.task_id,
            'task_name': self.task_name,
            'operator_id': self.operatorId,
            'sequence': self.sequence,
            'task_param': self.task_params,
            'operator': self.operator.to_dict() if self.operator is not None else {}
        }

class JobRequest:
    def __init__(self, job_name: str, cron: str, is_active: bool, environment: int, tasks: list[TaskRequest], job_id: int=0):
        self.job_name = job_name
        self.cron = cron
        self.is_active = is_active
        self.environment = environment
        self.tasks = tasks
        self.job_id = job_id

    def __repr__(self):
        return f"Job(job_name={self.job_name}, cron={self.cron}, is_active={self.is_active}, environment={self.environment}, tasks={self.tasks})"
    
    def to_dict(self):
        
        return {
            'job_id': self.job_id,
            'job_name': self.job_name,
            'cron_expression': self.cron,
            'is_active': self.is_active,
            'environment': self.environment,
            'tasks': [task.to_dict() for task in self.tasks]
        }

class Task:
    def __init__(self, task_id: int, task_name: str, operator_id: Operator, sequence: int, task_param: str):
        self.task_id = task_id
        self.task_name = task_name
        self.operator_id = operator_id
        self.sequence = sequence
        self.task_param = task_param

    def __repr__(self):
        return f"Task(task_name={self.task_name}, operator={self.operator}, sequence={self.sequence}, task_param={self.task_param})"


class Job:
    def __init__(self, job_id: int, job_name: str, cron_expression: str, is_active: bool, environment: int, tasks: list):
        self.job_id = job_id
        self.job_name = job_name
        self.cron_expression = cron_expression
        self.is_active = is_active
        self.environment = environment
        self.tasks = tasks
        self.created_on = datetime.datetime.now()
        self.modified_on = datetime.datetime.now()
        self.created_by = "System"
        self.modified_by = "System"

    def __repr__(self):
        return f"Job(job_name={self.job_name}, cron_expression={self.cron_expression}, is_active={self.is_active}, environment={self.environment}, tasks={self.tasks})"

