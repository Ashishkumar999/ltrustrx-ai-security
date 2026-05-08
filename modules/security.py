from datetime import datetime, timedelta


FAILED_LOGINS = {}

MAX_ATTEMPTS = 5

BLOCK_TIME_MINUTES = 1


def is_blocked(username):

    if username not in FAILED_LOGINS:
        return False

    attempts = FAILED_LOGINS[username]["attempts"]

    last_attempt = FAILED_LOGINS[username]["time"]

    if attempts >= MAX_ATTEMPTS:

        if datetime.now() < last_attempt + timedelta(minutes=BLOCK_TIME_MINUTES):
            return True

        FAILED_LOGINS.pop(username)

    return False


def record_failed_attempt(username):

    if username not in FAILED_LOGINS:

        FAILED_LOGINS[username] = {
            "attempts": 1,
            "time": datetime.now()
        }

    else:

        FAILED_LOGINS[username]["attempts"] += 1

        FAILED_LOGINS[username]["time"] = datetime.now()


def reset_attempts(username):

    if username in FAILED_LOGINS:
        FAILED_LOGINS.pop(username)
