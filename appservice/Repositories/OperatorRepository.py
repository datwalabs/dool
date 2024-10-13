from Repositories.DatabaseConnection import Database
from Models.JobModels import *

def get_all_operators():
    db = Database()
    db.connect()
    cursor = db.connection.cursor()

    cursor.execute("""
        SELECT * FROM Operator
    """)
    
    rows = cursor.fetchall()
    operators = []
    for row in rows:
        operator_id, operator_name, description, operator_slug = row
        operator = Operator(operator_name=operator_name, operator_slug=operator_slug, operator_id=operator_id, description=description)
        operators.append(operator.to_dict())
    
    return operators