import csv
import os

def generate_rel(file_name, pattern, count):
    if os.path.exists('main/'+file_name):
        print(f"⚠️ File '{file_name}' already exists. Skipping generation.")
        return

    with open(file_name, "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["col1", "col2"])  # header

        for i in range(1, count + 1):
            if pattern == "i-i":
                writer.writerow([i, i])
            elif pattern == "i-1":
                writer.writerow([i, 1])
            else:
                raise ValueError("Unknown pattern")

# generate_rel("main/Rel-i-i-1000.csv", "i-i", 1000)
# generate_rel("main/Rel-i-1-1000.csv", "i-1", 1000)
generate_rel("main/Rel-i-i-1000000.csv", "i-i", 100000)
generate_rel("main/Rel-i-1-1000000.csv", "i-1", 100000)