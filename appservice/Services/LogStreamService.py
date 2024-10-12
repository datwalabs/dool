import time
import os

LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "logs", "log101.log")
def hello():
    return "Hello"

def read_log_file():
    # Check if the log file exists
    if not os.path.isfile(LOG_FILE_PATH):
        yield "data: Log file not found.\n\n"
        return

    # First, read and send the entire log file content
    with open(LOG_FILE_PATH, 'r') as log_file:
        content = log_file.read()
        yield f"data: {content}\n\n"  # Send existing log content

    # Then, start reading new lines
    with open(LOG_FILE_PATH, 'r') as log_file:
        log_file.seek(0, 0)  # Start reading from the beginning of the file
        while True:
            line = log_file.readline()
            if not line:
                time.sleep(1)  # Sleep briefly if no new line is added
                continue
            yield f"data: {line}\n\n"  # Send new log line

