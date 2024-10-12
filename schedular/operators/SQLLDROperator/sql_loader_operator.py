import subprocess
from ..base_operator import BaseOperator
import os

class SQLLoaderOperator(BaseOperator):
    def __init__(self, task_id, description, control_file, data_file, log_file, bad_file, discard_file, oracle_home):
        super().__init__(task_id, description)
        self.control_file = control_file
        self.data_file = data_file
        self.log_file = log_file
        self.bad_file = bad_file
        self.discard_file = discard_file
        self.oracle_home = oracle_home

    def execute(self):
        try:
            # Construct SQL*Loader command
            sqlldr_cmd = f"{self.oracle_home}/bin/sqlldr control={self.control_file} data={self.data_file} log={self.log_file} bad={self.bad_file} discard={self.discard_file}"
            
            # Execute SQL*Loader
            result = subprocess.run(
                sqlldr_cmd,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                env={'ORACLE_HOME': self.oracle_home, 'PATH': f"{self.oracle_home}/bin:{os.environ['PATH']}"}
            )
            
            print(f"Task {self.task_id} output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing {self.task_id}: {e}")
            print(f"Error output: {e.stderr}")
            return False
