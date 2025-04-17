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

        # Case 1: Error message
        if isinstance(result, str) and result.startswith("Error:"):
            return [], [result], exec_time

        # Case 2: Already structured output
        if isinstance(result, dict) and "columns" in result and "rows" in result:
            return result["rows"], result["columns"], exec_time

        # Case 3: Convert tabular string output
        if isinstance(result, str) and "\n" in result:
            lines = result.strip().split("\n")
            if len(lines) >= 2 and "|" in lines[0]:
                header = [col.strip() for col in lines[0].split("|")]
                rows = [tuple(cell.strip() for cell in row.split("|")) for row in lines[2:]]
                return rows, header, exec_time

        # Case 4: Simple string message
        if isinstance(result, str):
            return [(result,)], ["Message"], exec_time

        # Fallback
        return [], ["No data returned"], exec_time

    except Exception as e:
        print("🔥 DEBUG ERROR:", type(e), e)
        import traceback
        traceback.print_exc()
        return f"Error: {str(e)}", 0.0
