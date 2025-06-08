# # backend/mcp/github_mcp.py

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()


# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
# GITHUB_API = "https://api.github.com"
# HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

# print("DEBUG: GITHUB_TOKEN =", GITHUB_TOKEN)

# def get_commits(repo: str):
#     url = f"{GITHUB_API}/repos/{repo}/commits"
#     res = requests.get(url, headers=HEADERS)
#     res.raise_for_status()
#     return res.json()


# def get_issues(repo: str):
#     url = f"{GITHUB_API}/repos/{repo}/issues"
#     res = requests.get(url, headers=HEADERS)
#     res.raise_for_status()
#     return res.json()


# def main():
#     repo = input("Введите репозиторий (в формате user/repo): ").strip()

#     print("\n🔄 Загружаем коммиты...")
#     commits = get_commits(repo)
#     for commit in commits[:5]:  # покажем первые 5
#         print(f"[COMMIT] {commit['sha'][:7]} - {commit['commit']['message']}")

#     print("\n🔄 Загружаем issues...")
#     issues = get_issues(repo)
#     for issue in issues[:5]:
#         print(f"[ISSUE] #{issue['number']} - {issue['title']}")


# if __name__ == "__main__":
#     main()


import os
import requests
from dotenv import load_dotenv

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_API = "https://api.github.com"
HEADERS = {"Authorization": f"token {GITHUB_TOKEN}"}

def get_commits(repo: str):
    url = f"{GITHUB_API}/repos/{repo}/commits"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()

def get_issues(repo: str):
    url = f"{GITHUB_API}/repos/{repo}/issues"
    res = requests.get(url, headers=HEADERS)
    res.raise_for_status()
    return res.json()
