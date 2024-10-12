import os
from .base_operator import BaseOperator
import json

class PythonOperator(BaseOperator):
    def __init__(self, task_id, description, filepath, max_retries=2, env=None):
        super().__init__(task_id, description)
        self.filepath = filepath
        self.max_retries = max_retries
        self.env = env

#retry_on_failure
    def execute(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        retries = 0
        while retries < self.max_retries:
            try:
                # Prepare the execution environment
                exec_env = os.environ.copy()
                exec_env.update(self.env)
                
                # Execute the Python script and capture its output
                with open(self.filepath, 'r') as file:
                    code = file.read()
                
                local_vars = {}
                exec(code, {'__builtins__': __builtins__, 'env': exec_env}, local_vars)
                
                # Prepare the output dictionary
                output = {'data': local_vars.get('result', None)}
                
                # Store the output in the environment variable
                env_var_name = f"python_{self.task_id}"
                os.environ[env_var_name] = json.dumps(output)
                
                print(f"Output saved to environment variable: {env_var_name}")
                return True
            except Exception as e:
                print(f"Error executing {self.task_id}: {str(e)}")
                retries += 1
        
        return False
