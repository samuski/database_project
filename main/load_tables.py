import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DBMS_ROOT = os.path.abspath("dbms")
DB_PATH = os.path.join(DBMS_ROOT, "database")

# Add DBMS submodule to Python path
DBMS_DIR = os.path.abspath("dbms")
sys.path.insert(0, DBMS_DIR)

from dbms.main import DBMSApplication

# Initialize DBMS app
app = DBMSApplication(db_directory="/app/dbms/database")

# Your CSV directory
csv_dir = os.path.join(SCRIPT_DIR, "data_files")

file = 'million_1.csv'
table = file[:-4]  # filename without .csv
full_path = os.path.join(csv_dir, file)
command = f"COPY {table} FROM '{full_path}' CSV"
print(f"Loading into table '{table}'...")
app._execute_copy_command(command)
