from neo4j import GraphDatabase

class Neo4jConnector:
    def __init__(self, uri="bolt://localhost:7687", user="neo4j", password="password"):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def run(self, query, parameters=None):
        with self.driver.session() as session:
            return session.run(query, parameters or {})

    def close(self):
        self.driver.close()

# ес че говорит аишка вот так юзать эту хуету
# from graph.neo4j_connector import Neo4jConnector
# conn = Neo4jConnector()
# conn.run("MATCH (n) RETURN COUNT(n)")
# conn.close()
