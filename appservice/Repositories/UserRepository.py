# user_service.py
from flask import request
from Repositories.DatabaseConnection import Database
from Models.UserModels import *

def create_user(user: CreateUserRequest):
    # Define your database connection details
    db = Database()

    procedure_name = 'CreateUser'  # Name of your stored procedure
    params = (user.username, user.email, user.password)
    
    try:
        result = db.execute_stored_procedure(procedure_name, params)
        print(result)
        return result  # Modify this depending on what the stored procedure returns
    finally:
        db.close()

def sign_in_user(user):
    pass

def get_all_users():
    pass