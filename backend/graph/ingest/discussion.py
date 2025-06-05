def ingest_discussion(conn, discussion: dict, project_id: str):
    conn.run("""
        MERGE (d:Discussion {id: $id})
        SET d.topic = $topic,
            d.summary = $summary,
            d.date = date($date),
            d.source_url = $source_url

        MERGE (p:Project {id: $project_id})
        MERGE (p)-[:HAS]->(d)

        FOREACH (email IN $participants |
            MERGE (u:User {id: email})
            MERGE (u)-[:PARTICIPATED_IN]->(d)
        )
    """, {
        "id": discussion["id"],
        "topic": discussion["topic"],
        "summary": discussion.get("summary", ""),
        "date": discussion["date"],
        "source_url": discussion["source_url"],
        "participants": discussion["participants"],
        "project_id": project_id
    })
