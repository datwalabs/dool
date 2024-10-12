import os
import sqlalchemy
from ..base_operator import BaseOperator

class DBOperator(BaseOperator):
    def __init__(self, task_id, description, db_config, sql_query):
        super().__init__(task_id, description)
        self.db_config = db_config
        self.sql_query = sql_query

    def execute(self):
        try:
            # Create connection string
            conn_str = f"{self.db_config['dialect']}://{self.db_config['username']}:{self.db_config['password']}@{self.db_config['host']}:{self.db_config['port']}/{self.db_config['database']}"
            
            # Create engine
            engine = sqlalchemy.create_engine(conn_str)
            
            # Execute query
            with engine.connect() as connection:
                result = connection.execute(sqlalchemy.text(self.sql_query))
                
                # Process results if needed
                for row in result:
                    print(row)
            
            return True
        except Exception as e:
            print(f"Error executing {self.task_id}: {str(e)}")
            return False
