import subprocess
from ..base_operator import BaseOperator

class BashOperator(BaseOperator):
    def __init__(self, task_id, description, bash_command, env=None):
        super().__init__(task_id, description)
        self.bash_command = bash_command
        self.env = env

    def execute(self):
        try:
            result = subprocess.run(
                self.bash_command,
                shell=True,
                check=True,
                capture_output=True,
                text=True,
                env=self.env
            )
            print(f"Task {self.task_id} output: {result.stdout}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Error executing {self.task_id}: {e}")
            print(f"Error output: {e.stderr}")
            return False
