from neo4j import GraphDatabase

NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "neo4j123"

class GraphSchemaInitializer:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run(self):
        with self.driver.session() as session:
            session.execute_write(self.create_constraints)

    @staticmethod
    def create_constraints(tx):
        constraints = [
            ("User", "id"),
            ("Project", "id"),
            ("TrelloCard", "id"),
            ("GitHubIssue", "id"),
            ("PullRequest", "id"),
            ("Commit", "sha"),
            ("Branch", "name"),
            ("Component", "name"),
            ("Discussion", "id"),
            ("Release", "name"),
            ("Document", "id"),
            ("LLMTask", "id"),
        ]

        for label, field in constraints:
            query = (
                f"CREATE CONSTRAINT IF NOT EXISTS "
                f"FOR (n:{label}) REQUIRE n.{field} IS UNIQUE"
            )
            tx.run(query)

if __name__ == "__main__":
    initializer = GraphSchemaInitializer(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    initializer.run()
    initializer.close()
    print("Graph schema initialized.")