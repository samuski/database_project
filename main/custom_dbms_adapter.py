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

        # Case: error message from run_query
        if isinstance(result, str) and result.startswith("Error:"):
            return [], [result], exec_time

        # Structured result from _format_result()
        if isinstance(result, dict) and "columns" in result and "rows" in result:
            return result["rows"], result["columns"], exec_time

        # Fallback
        return [], ["No data returned"], exec_time

    except Exception as e:
        return [], [f"Error: {str(e)}"], 0.0

def copy_from_csv(self, table_name, csv_path, has_header=True):
    return self.executor.copy_from_csv(table_name, csv_path, has_header)
