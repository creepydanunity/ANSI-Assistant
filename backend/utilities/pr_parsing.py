import httpx

from utilities.chunking import get_file_content


async def fetch_changed_files(url: str, token: str):
    headers = {
        "Authorization": f"token {token}",
    }
    params = {"per_page": 100}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    
async def categorize_files(owner: str, repo: str, files, token: str):
    categorized = {"added": [], "modified": [], "removed": [], "renamed": []}
    for file in files:
        status = file["status"]
        full_file_path = file["filename"]

        if status == "renamed":
            old_file_path = file.get("previous_filename")
            if old_file_path:
                categorized["renamed"].append({
                    "old_path": old_file_path,
                    "path": full_file_path
                })
        elif status == "removed":
            categorized["removed"].append({
                "path": full_file_path
            })
        elif status in categorized:
            file_content = await get_file_content(owner, repo, full_file_path, token)
            file_info = {
                "path": full_file_path,
                "content": file_content
            }
            categorized[status].append(file_info)

    return categorized