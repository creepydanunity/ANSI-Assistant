import re
from datetime import datetime
import dateparser

def parse_reminder_intent(text: str) -> dict:
    # Naive verb extraction
    match = re.search(r"remind me to (.+?) on|at|by", text, re.IGNORECASE)
    action = match.group(1).strip() if match else "unknown"

    dt = dateparser.parse(text)
    if not dt:
        raise ValueError("Could not parse datetime from input.")

    return {
        "action": action,
        "datetime": dt,
        "repeat": None,
        "raw_text": text
    }
