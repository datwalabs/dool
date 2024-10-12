# db_connection.py
import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "192.168.29.31"
        self.database = "dool"
        self.user = "test"
        self.password = "test"
        self.connection = None

    def connect(self):
        if self.connection is None:
            try:
                self.connection = mysql.connector.connect(
                    host=self.host,
                    database=self.database,
                    user=self.user,
                    password=self.password
                )
                if self.connection.is_connected():
                    print("Connected to MySQL database")
            except Error as e:
                print(f"Error: {e}")

    def close(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection to MySQL database closed")

    def execute_stored_procedure(self, procedure_name, params=None):
        self.connect()
        cursor = self.connection.cursor()
        try:
            if params:
                cursor.callproc(procedure_name, params)
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                return results
            else:
                cursor.callproc(procedure_name)
                results = []
                for result in cursor.stored_results():
                    results.extend(result.fetchall())
                return results
        except Error as e:
            print(f"Error executing stored procedure: {e}")
        finally:
            cursor.close()


db = Database()
db.connect()