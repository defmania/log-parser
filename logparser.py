import csv
from datetime import datetime

LOG_FILE = "logs.csv"
REPORT = "output.txt"
ERROR_THRESHOLD = 600
WARNING_THRESHOLD = 300


def parse_log(file_path):
    jobs = {} # Dictionary to store job details

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            timestamp, task_name, status, pid = row
            timestamp = datetime.strptime(timestamp, "%H:%M:%S")

            if pid not in jobs:
                jobs[pid] = {"name": task_name, "start": None, "end": None}

            if status == "START":
                jobs[pid]["start"] = timestamp
            elif status == "END":
                jobs[pid]["end"] = timestamp
            print(f"DEBUG: {timestamp} - {task_name} - {status} - {pid}") # Debugging print

    return jobs

# Funtion to analyze jobs and write to report file

def analyze_jobs(jobs, report_file):
    with open(output_file, "w") as f:


if __name__ == "__main__":
    job_data = parse_log(LOG_FILE)
