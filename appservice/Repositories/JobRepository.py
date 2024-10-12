from Repositories.DatabaseConnection import Database
from Models.JobModels import *

def create_job(job: JobRequest):
    # Define your database connection details
    db = Database()
    db.connect()
    cursor = db.connection.cursor()

    # Insert job data
    cursor.execute("""
        INSERT INTO jobs (job_name, cron_expression, is_active, environment, created_on, modified_on, created_by, modified_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (job.job_name, job.cron, job.is_active, job.environment, datetime.datetime.now(), datetime.datetime.now(), "System", "System"))
    
    # Get the last inserted job ID
    job_id = cursor.lastrowid
    job.job_id = job_id
    
    for i in range(len(job.tasks)):
        task = job.tasks[i]
        task_name = task.task_name
        operator_id = task.operatorId
        sequence = task.sequence
        task_param = task.task_params

        cursor.execute("""
            INSERT INTO tasks (job_id, task_name, operator_id, sequence, task_param)
            VALUES (%s, %s, %s, %s, %s)
        """, (job_id, task_name, operator_id, sequence, task_param))
        task_id = cursor.lastrowid
        job.tasks[i].task_id = task_id
        
    
    
    db.connection.commit()
    cursor.close()
    db.close()
    
    return job

def update_job(job: JobRequest):
    # Define your database connection details
    db = Database()
    db.connect()
    cursor = db.connection.cursor()

    # Update job data
    cursor.execute("""
        UPDATE jobs
        SET job_name = %s, cron_expression = %s, is_active = %s, environment = %s, modified_on = %s, modified_by = %s
        WHERE job_id = %s
    """, (job.job_name, job.cron, job.is_active, job.environment, datetime.datetime.now(), "System", job.job_id))

    # Delete all existing tasks for the job
    cursor.execute("""
        DELETE FROM tasks
        WHERE job_id = %s
    """, (job.job_id,))

    # Insert new tasks
    for task in job.tasks:
        cursor.execute("""
            INSERT INTO tasks (job_id, task_name, operator_id, sequence, task_param)
            VALUES (%s, %s, %s, %s, %s)
        """, (job.job_id, task.task_name, task.operatorId, task.sequence, task.task_params))
        task.task_id = cursor.lastrowid  # Update the task_id with the new ID

    db.connection.commit()
    cursor.close()
    db.close()

    return job

def get_all_jobs():
    db = Database()
    db.connect()
    cursor = db.connection.cursor()

    cursor.execute("""
        SELECT 
            j.job_id, j.job_name, j.cron_expression, j.is_active, j.environment,
            t.task_id, t.task_name, o.operator_id, o.operator_name, o.operator_slug, o.description, 
            t.sequence, t.task_param
        FROM jobs j
        LEFT JOIN tasks t ON j.job_id = t.job_id
        LEFT JOIN operator o ON t.operator_id = o.operator_id
    """)
    
    rows = cursor.fetchall()
    
    jobs = {}
    for row in rows:
        job_id, job_name, cron_expression, is_active, environment, task_id, task_name, operator_id, operator_name, operator_slug, operator_description, sequence, task_param = row
        
        if job_id not in jobs:
            jobs[job_id] = JobRequest(
                job_id=job_id,
                job_name=job_name,
                cron=cron_expression,
                is_active=is_active,
                environment=environment,
                tasks=[]
            )
        
        
        if task_id is not None:
            operator = Operator(
                operator_name=operator_name,
                operator_slug=operator_slug,
                operator_id=operator_id,
                description=operator_description
            )
            
            task = TaskRequest(
                task_id=task_id,
                task_name=task_name,
                operator=operator,
                sequence=sequence,
                task_params=task_param,
                operatorId = operator_id,
            )
            jobs[job_id].tasks.append(task)
        jobs[job_id] = jobs[job_id].to_dict()

    cursor.close()
    db.close()

    return list(jobs.values())

def get_job_by_id(job_id: int):
    db = Database()
    db.connect()
    cursor = db.connection.cursor()

    cursor.execute("""
        SELECT 
            j.job_id, j.job_name, j.cron_expression, j.is_active, j.environment,
            t.task_id, t.task_name, o.operator_id, o.operator_name, o.operator_slug, o.description, 
            t.sequence, t.task_param
        FROM jobs j
        LEFT JOIN tasks t ON j.job_id = t.job_id
        LEFT JOIN operator o ON t.operator_id = o.operator_id
        WHERE j.job_id = %s
    """, (job_id,))
    
    rows = cursor.fetchall()
    
    if not rows:
        cursor.close()
        db.close()
        return None  # No job found with the given ID

    job = None
    for row in rows:
        if job is None:
            job_id, job_name, cron_expression, is_active, environment, _, _, _, _, _, _, _,_ = row
            job = JobRequest(
                job_id=job_id,
                job_name=job_name,
                cron=cron_expression,
                is_active=is_active,
                environment=environment,
                tasks=[]
            )
        
        task_id, task_name, operator_id, operator_name, operator_slug, operator_description, sequence, task_param = row[5:]
        
        if task_id is not None:
            operator = Operator(
                operator_name=operator_name,
                operator_slug=operator_slug,
                operator_id=operator_id,
                description=operator_description
            )
            
            task = TaskRequest(
                task_id=task_id,
                task_name=task_name,
                operator=operator,
                sequence=sequence,
                task_params=task_param,
                operatorId=operator_id
            )
            job.tasks.append(task)

    cursor.close()
    db.close()

    return job.to_dict()