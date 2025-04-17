import os
import glob
from django.db import connection
from django.core.management.base import BaseCommand
from main.data_files.init_database import load_tables, table_init
from main.custom_dbms_adapter import run_custom_query

class Command(BaseCommand):
    help = "Automatically import CSV data into the database if not already imported."

    def is_data_imported():
        rows, columns, _ = run_custom_query("SELECT COUNT(*) FROM crime;")
    #   with connection.cursor() as cursor:
    #       cursor.execute("SELECT COUNT(*) FROM crime;")
    #       count = cursor.fetchone()[0]
        return int(rows[0][0]) > 0 if rows else False


    def handle(self, *args, **options):
        table_init() # Error proofed with IF NOT EXISTS
        count = run_custom_query("SELECT COUNT(*) FROM crime;")
        rows, columns, _ = run_custom_query("SELECT COUNT(*) FROM crime;")
        count = int(rows[0][0]) if rows else 0
        
        # with connection.cursor() as cursor:
        #   cursor.execute("SELECT COUNT(*) FROM crime;")
        #   count = cursor.fetchone()[0]

        # Check if data has already been imported by inspecting the crime table.
        if count == 0:
            # Set the directory where your CSV files reside.
            # Adjust the path so it correctly points to your data_files directory.
            BASE_DIR = os.path.dirname(os.path.abspath(__file__))
            csv_directory = os.path.join(BASE_DIR, "..", "..", "data_files")
            
            master_file = None
            csv_files = glob.glob(os.path.join(csv_directory, "*.csv"))
            
            # Process all CSV files except "crime.csv" first.
            for csv_file in csv_files:
                if os.path.basename(csv_file).lower() == "crime.csv":
                    master_file = csv_file
                else:
                    load_tables(csv_file)
            
            # Process "crime.csv" last due to foreign key dependencies.
            if master_file:
                load_tables(master_file)
            
            self.stdout.write(self.style.SUCCESS("CSV data imported successfully."))
        else:
            self.stdout.write("Data already imported, skipping.")
