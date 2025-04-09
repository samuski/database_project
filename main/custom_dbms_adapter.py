import os
import sys

# Add DBMS submodule to Python path
DBMS_DIR = os.path.abspath("dbms")
sys.path.insert(0, DBMS_DIR)

from dbms.main import DBMSApplication

# Instantiate once
_app = DBMSApplication(db_directory=os.path.join(DBMS_DIR, 'database'))

def run_custom_query(sql_query):
    try:
        result, exec_time = _app.run_query(sql_query)
        
        # Return a list of rows and list of column names
        if isinstance(result, list) and len(result) > 0:
            # If result is a list of dictionaries or tuples, extract columns
            if isinstance(result[0], dict):
                columns = list(result[0].keys())
                rows = [tuple(row.values()) for row in result]
            elif isinstance(result[0], tuple):
                rows = result
                columns = [f"col_{i}" for i in range(len(rows[0]))]
            else:
                rows = [(item,) for item in result]
                columns = ["result"]
        else:
            rows = []
            columns = []

        return rows, columns

    except Exception as e:
        return [], [f"Error: {str(e)}"]
