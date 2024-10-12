from abc import ABC, abstractmethod

class BaseOperator(ABC):
    def __init__(self, task_id, description):
        self.task_id = task_id
        self.description = description

    @abstractmethod
    def execute(self):
        pass
