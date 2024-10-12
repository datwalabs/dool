'''
Note: Written in DB first. Each model class has to mimic the table in DB. No business logic must be involved in a model method
'''
import hashlib

class Environment:
    def __init__(self, environment_id: int, environment_name: str):
        self.environment_id = environment_id
        self.environment_name = environment_name

    def __repr__(self):
        return f"Environment(id={self.environment_id}, name='{self.environment_name}')"

class Job:
    def __init__(self, job_id: int, job_name: str):
        self.job_id = job_id
        self.job_name = job_name

    def __repr__(self):
        return f"Job(id={self.job_id}, name='{self.job_name}')"

class Role:
    def __init__(self, role_id: int, role_name: str, role_type: str, role_level: str, environments: list, jobs: list):
        self.role_id = role_id
        self.role_name = role_name
        self.role_type = role_type
        self.role_level = role_level
        self.environments = environments

    def __repr__(self):
        return (f"Role(id={self.role_id}, name='{self.role_name}', type='{self.role_type}', "
                f"level='{self.role_level}', environments={self.environments}, jobs={self.jobs})")

