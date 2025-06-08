from datetime import datetime
import re


def extract_json_from_response(response_text: str | None) -> str | None:
    # Remove Markdown-style code block if present
    if response_text is not None:
        match = re.search(r"```json\s*(.*?)```", response_text, re.DOTALL)
        if match:
            return match.group(1).strip()
        return response_text.strip()
    return None

def merge_backlog_from_tasks(task_list: list):
    last_updated = task_list[0]['source_date'] if task_list else datetime.now().strftime("%Y-%m-%d")
    result = {}
    for item in task_list:
        title = item['title']
        block = [
            f"## {title}\n",
            f"- Status: {item['status']}\n",
            f"- Last updated: {last_updated}\n",
            f"- Summary: {item['summary']}\n",
            f"- History:\n"
        ]
        for entry in item['history']:
            block.append(f"  - {entry['date']}: {entry['description']}\n")
        if 'alerts' in item and item['alerts']:
            block.append(f"- Alerts:\n")
            for alert in item['alerts']:
                block.append(f"  - {alert['date']}: {alert['issue']}\n")
        block.append("\n")
        result[title] = block
    return result