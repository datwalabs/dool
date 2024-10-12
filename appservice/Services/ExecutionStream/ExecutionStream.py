import time
import json
from flask import jsonify
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

# Database connection string (replace with your actual connection string)
DB_CONNECTION_STRING = "mysql://root:@localhost/worker_heartbeat"

engine = create_engine(DB_CONNECTION_STRING)

def serialize_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type not serializable")

def get_job_status(job_id):
    query = text("""
        SELECT 
            job_id, job_name, start_time, end_time, current_task, 
            current_task_start_time, current_task_status, is_failed, 
            error_task_id, error_message, retry_count, last_retry_time, 
            status, logfile_id, created_at, updated_at
        FROM job_execution
        WHERE job_id = :job_id
    """)
    
    try:
        with engine.connect() as connection:
            result = connection.execute(query, {"job_id": job_id}).fetchone()
            if result:
                job_status = {column: value for column, value in result._mapping.items()}
                # Convert datetime objects to ISO format strings
                for key, value in job_status.items():
                    if isinstance(value, datetime):
                        job_status[key] = value.isoformat()
                return job_status
            return None
    except SQLAlchemyError as e:
        print(f"Database error: {str(e)}")
        return None

def job_status_stream(job_id):
    while True:
        try:
            job_status = get_job_status(job_id)
        
            if job_status:
                yield f"data: {json.dumps(job_status)}\n\n"
            else:
                error_message = {"error": "Job not found or database error"}
                yield f"data: {json.dumps(error_message)}\n\n"
            
            # Check if the job has completed or failed
            if job_status and job_status['status'] in ['success', 'failed']:
                break
        except Exception as e:
            error_message = {"error": f"Error fetching job status for job_id {job_id}: {str(e)}"}
            yield f"data: {json.dumps(error_message)}\n\n"
        
        time.sleep(10)  # Wait for 10 seconds before the next update

def create_job_status_stream(job_id):
    def generate():
        return job_status_stream(job_id)
    
    return generate

# Example usage in a Flask route
# @app.route('/job_status/<int:job_id>')
# def stream_job_status(job_id):
#     return Response(create_job_status_stream(job_id)(), content_type='text/event-stream')