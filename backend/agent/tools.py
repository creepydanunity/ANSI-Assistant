# agent/tools.py

from mcp import github_mcp

def load_github_repo(repo: str) -> str:
    try:
        commits = github_mcp.get_commits(repo)
        issues = github_mcp.get_issues(repo)
        return f"Fetched {len(commits)} commits and {len(issues)} issues from '{repo}'."
    except Exception as e:
        return f"❌ Error fetching data from '{repo}': {str(e)}"

TOOL_FUNCTIONS = {
    "load_github_repo": load_github_repo
}
