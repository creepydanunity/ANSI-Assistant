def ingest_issue(conn, issue: dict, project_id: str):
    """
    Добавляет GitHub Issue и связывает его с проектом.
    """
    conn.run("""
        MERGE (i:GitHubIssue {id: $id})
        SET i.title = $title,
            i.url = $url,
            i.state = $state

        MERGE (p:Project {id: $project_id})
        MERGE (p)-[:HAS]->(i)
    """, {
        "id": issue["id"],
        "title": issue.get("title", ""),
        "url": issue.get("html_url", ""),
        "state": issue.get("state", "open"),
        "project_id": project_id
    })


def ingest_pull_request(conn, pr: dict, issue_id: str):
    """
    Добавляет Pull Request и связывает его с Issue.
    """
    conn.run("""
        MERGE (pr:PullRequest {id: $id})
        SET pr.title = $title,
            pr.url = $url

        MATCH (i:GitHubIssue {id: $issue_id})
        MERGE (i)-[:RESOLVED_BY]->(pr)
    """, {
        "id": pr["id"],
        "title": pr.get("title", ""),
        "url": pr.get("html_url", ""),
        "issue_id": issue_id
    })


def ingest_commit(conn, commit: dict, pr_id: str, branch_name: str, component_name: str = ""):
    """
    Добавляет Commit, связывает его с PR, веткой, автором и компонентом.
    """
    conn.run("""
        MERGE (c:Commit {sha: $sha})
        SET c.message = $message,
            c.timestamp = datetime($timestamp)

        MERGE (pr:PullRequest {id: $pr_id})
        MERGE (pr)-[:CONTAINS]->(c)

        MERGE (b:Branch {name: $branch_name})
        MERGE (c)-[:PART_OF]->(b)

        MERGE (u:User {id: $author})
        MERGE (u)-[:WROTE]->(c)

        FOREACH (_ IN CASE WHEN $component_name IS NOT NULL THEN [1] ELSE [] END |
            MERGE (m:Component {name: $component_name})
            MERGE (c)-[:TOUCHES]->(m)
        )
    """, {
        "sha": commit["sha"],
        "message": commit.get("commit", {}).get("message", ""),
        "timestamp": commit.get("commit", {}).get("author", {}).get("date", ""),
        "pr_id": pr_id,
        "branch_name": branch_name,
        "author": commit.get("author", {}).get("login", "unknown"),
        "component_name": component_name
    })
