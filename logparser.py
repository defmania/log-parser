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
            #cleaning up empty spaces
            pid = str(pid).strip()
            status = status.strip()
            timestamp = datetime.strptime(timestamp.strip(), "%H:%M:%S")
            #checking if pid is already in jobs dict
            if pid not in jobs:
                jobs[pid] = {"name": task_name, "start": None, "end": None}
            #updating start and end times for each job
            if status == "START":
                jobs[pid]["start"] = timestamp
            elif status == "END":
                jobs[pid]["end"] = timestamp
            print(f"DEBUG: {timestamp} - {task_name} - {status} - {pid}") # Debugging print of elements of dict

    return jobs

# Funtion to analyze jobs and write to report file

def analyze_jobs(jobs, report):
    with open(report, "w") as f:
        #add identified jobs to report
        f.write("Jobs...\n")
        #going through each job by pid and writing to output report the job name, start and end time
        for pid, details in jobs.items():
            startt = details["start"].strftime("%H:%M:%S") if details["start"] else "none"
            endd = details["end"].strftime("%H:%M:%S") if details["end"] else "none"
            f.write(f"- Job {details['name']} (PID {pid}) | Start: {startt} | End: {endd}\n")

        #analyzing jobs and writing to report
        f.write("\nAnalysis:\n")
        for pid, details in jobs.items():
            if details["start"] and details["end"]:
                duration = (details["end"] - details["start"]).total_seconds()
                duration_str = f"{int(duration // 60)} min {int(duration % 60)} sec"
                print(f"DEBUG: Job {details['name']} (PID {pid}) lasted {duration} seconds")

                if duration > ERROR_THRESHOLD:
                    f.write(f"ERROR: Job {details['name']} (PID {pid}) took {duration_str}!\n")
                elif duration > WARNING_THRESHOLD:
                    f.write(f"WARNING: Job {details['name']} (PID {pid}) took {duration_str}!\n")
                """ else:
                    f.write(f"INFO: Job {details['name']} (PID {pid}) completed in {duration_str}.\n") """


if __name__ == "__main__":
    job_data = parse_log(LOG_FILE)
    analyze_jobs(job_data, REPORT)
