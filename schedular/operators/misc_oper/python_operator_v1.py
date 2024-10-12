import os
import subprocess
import json
import time
from datetime import datetime
from ..base_operator import BaseOperator

class PythonOperator(BaseOperator):
    def __init__(self, task_id, description, filepath, env, **kwargs):
        super().__init__(task_id, description)
        self.filepath = filepath
        self.env = env
        self.config = {
            "script_path": filepath,
            "execution_mode": kwargs.get("execution_mode", "blocking"),
            "timeout": kwargs.get("timeout", 3600),
            "retry_count": kwargs.get("retry_count", 3),
            "retry_delay": kwargs.get("retry_delay", 300),
            "python_version": kwargs.get("python_version", "3.8"),
            "virtualenv_path": kwargs.get("virtualenv_path"),
            "dependencies": kwargs.get("dependencies", []),
            "schedule": kwargs.get("schedule"),
            "trigger_event": kwargs.get("trigger_event", "manual"),
            "input_parameters": kwargs.get("input_parameters", {}),
            "output_location": kwargs.get("output_location"), #s3 or local file path
            "capture_output": kwargs.get("capture_output", True),
            "alert_on_failure": kwargs.get("alert_on_failure", True),
            "alert_channels": kwargs.get("alert_channels", ["email"]),
            "logs_path": kwargs.get("logs_path"),
            "execution_user": kwargs.get("execution_user"),
            "isolation_mode": kwargs.get("isolation_mode"),
            "resource_limits": kwargs.get("resource_limits", {}),
            "concurrency": kwargs.get("concurrency", 1),
            "task_priority": kwargs.get("task_priority", 1),
            "execution_context": {
                "task_id": task_id,
                "triggered_by": kwargs.get("triggered_by", "system")
            },
            "execution_history": kwargs.get("execution_history", []),
            "audit_trail": {
                "triggered_by": kwargs.get("triggered_by", "system"),
                "timestamp": datetime.utcnow().isoformat() + "Z"
            }
        }

    def execute(self):
        if not os.path.exists(self.filepath):
            raise FileNotFoundError(f"File not found: {self.filepath}")
        
        retries = 0
        while retries < self.config["retry_count"]:
            try:
                result = self._run_script()
                self._update_execution_history("success")
                return result
            except Exception as e:
                print(f"Error executing {self.task_id}: {str(e)}")
                retries += 1
                if retries < self.config["retry_count"]:
                    time.sleep(self.config["retry_delay"])
                else:
                    self._update_execution_history("failure")
                    if self.config["alert_on_failure"]:
                        self._send_alert(str(e))
        
        return False

    def _run_script(self):
        cmd = [self.config["python_version"], self.filepath]
        
        if self.config["virtualenv_path"]:
            activate_this = f"{self.config['virtualenv_path']}/bin/activate_this.py"
            exec(open(activate_this).read(), {'__file__': activate_this})

        for dep in self.config["dependencies"]:
            subprocess.check_call(["pip", "install", "-r", dep])

        env = os.environ.copy()
        env.update(self.env)
        env.update(self.config["input_parameters"])

        if self.config["isolation_mode"] == "docker":
            # Implement Docker execution logic here
            pass
        else:
            process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            try:
                stdout, stderr = process.communicate(timeout=self.config["timeout"])
                if self.config["capture_output"]:
                    self._save_output(stdout, stderr)
                return process.returncode == 0
            except subprocess.TimeoutExpired:
                process.kill()
                raise Exception("Execution timed out")

    def _save_output(self, stdout, stderr):
        if self.config["output_location"]:
            with open(f"{self.config['output_location']}/{self.task_id}_stdout.log", "w") as f:
                f.write(stdout)
            with open(f"{self.config['output_location']}/{self.task_id}_stderr.log", "w") as f:
                f.write(stderr)

    def _update_execution_history(self, status):
        self.config["execution_history"].append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": status
        })

    def _send_alert(self, error_message):
        # Implement alert logic here (e.g., send email, Slack message)
        pass