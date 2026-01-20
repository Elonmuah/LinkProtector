import json
from datetime import datetime
from pathlib import Path

def logError(error):
    path = Path("errorLog.json")
    
    # Load existing logs or start empty
    if path.exists():
        with open(path, "r") as f:
            logs = json.load(f)
    else:
        logs = []

    # Append the new error
    logs.append(error)

    # Sort logs by date ascending (oldest first)
    logs_sorted = sorted(
        logs,
        key=lambda x: datetime.fromisoformat(x["time"].replace("Z", "+00:00"))
    )

    # Write back sorted logs, with keys inside each object sorted
    with open(path, "w") as f:
        json.dump(logs_sorted, f, indent=4, sort_keys=True)