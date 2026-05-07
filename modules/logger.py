from datetime import datetime


LOG_FILE = "logs/security.log"


def write_log(event, username="anonymous"):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    log_entry = f"[{timestamp}] USER={username} EVENT={event}\n"

    with open(LOG_FILE, "a") as file:

        file.write(log_entry)
