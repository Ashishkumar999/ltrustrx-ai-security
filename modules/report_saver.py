import json
from datetime import datetime
import os


def generate_summary(issues):

    summary = {
        "total": len(issues),
        "high": 0,
        "medium": 0,
        "low": 0,
        "info": 0
    }

    for issue in issues:

        severity = issue.get("severity", "").lower()

        if severity == "high":
            summary["high"] += 1

        elif severity == "medium":
            summary["medium"] += 1

        elif severity == "low":
            summary["low"] += 1

        elif severity == "info":
            summary["info"] += 1

    return summary

def save_report(data):
    os.makedirs("reports", exist_ok=True)

    filename = f"reports/report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

    return filename
