import json
import os
from datetime import datetime


LOG_DIR = "backend/app/logs"
LOG_FILE = f"{LOG_DIR}/requests.jsonl"


def log_request(data: dict):
    """
    Append request log to JSONL file
    """

    os.makedirs(LOG_DIR, exist_ok=True)

    log_entry = {
        "timestamp": datetime.utcnow().isoformat(),
        **data
    }

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(log_entry) + "\n")