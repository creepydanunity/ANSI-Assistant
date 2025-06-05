// === NODE TYPES ===

CREATE CONSTRAINT user_id IF NOT EXISTS
ON (u:User) ASSERT u.id IS UNIQUE;

CREATE CONSTRAINT project_id IF NOT EXISTS
ON (p:Project) ASSERT p.id IS UNIQUE;

CREATE CONSTRAINT card_id IF NOT EXISTS
ON (c:TrelloCard) ASSERT c.id IS UNIQUE;

CREATE CONSTRAINT issue_id IF NOT EXISTS
ON (i:GitHubIssue) ASSERT i.id IS UNIQUE;

CREATE CONSTRAINT pr_id IF NOT EXISTS
ON (pr:PullRequest) ASSERT pr.id IS UNIQUE;

CREATE CONSTRAINT commit_sha IF NOT EXISTS
ON (c:Commit) ASSERT c.sha IS UNIQUE;

CREATE CONSTRAINT branch_name IF NOT EXISTS
ON (b:Branch) ASSERT b.name IS UNIQUE;

CREATE CONSTRAINT component_name IF NOT EXISTS
ON (c:Component) ASSERT c.name IS UNIQUE;

CREATE CONSTRAINT discussion_id IF NOT EXISTS
ON (d:Discussion) ASSERT d.id IS UNIQUE;

CREATE CONSTRAINT release_name IF NOT EXISTS
ON (r:Release) ASSERT r.name IS UNIQUE;

CREATE CONSTRAINT document_id IF NOT EXISTS
ON (d:Document) ASSERT d.id IS UNIQUE;

CREATE CONSTRAINT llmtask_id IF NOT EXISTS
ON (t:LLMTask) ASSERT t.id IS UNIQUE;

// === RELATIONSHIPS ===

/*
(:User)-[:OWNS]->(:Project)
(:User)-[:ASSIGNED_TO]->(:TrelloCard)
(:User)-[:WROTE]->(:Commit)
(:User)-[:PARTICIPATED_IN]->(:Discussion)
(:User)<-[:GEN_FOR]-(:LLMTask)
*/

CALL db.createRelationshipType('OWNS');
CALL db.createRelationshipType('ASSIGNED_TO');
CALL db.createRelationshipType('WROTE');
CALL db.createRelationshipType('PARTICIPATED_IN');
CALL db.createRelationshipType('GEN_FOR');

/*
(:Project)-[:HAS]->(:TrelloCard|:GitHubIssue|:Discussion|:Document|:Release)
*/

CALL db.createRelationshipType('HAS');

/*
(:TrelloCard)-[:LINKED_TO]->(:GitHubIssue)
(:TrelloCard)<-[:CREATED_FROM]-(:Discussion)
*/

CALL db.createRelationshipType('LINKED_TO');
CALL db.createRelationshipType('CREATED_FROM');

/*
(:GitHubIssue)-[:RESOLVED_BY]->(:PullRequest)
(:GitHubIssue)<-[:DISCUSSED_IN]-(:Discussion)
*/

CALL db.createRelationshipType('RESOLVED_BY');
CALL db.createRelationshipType('DISCUSSED_IN');

/*
(:PullRequest)-[:CONTAINS]->(:Commit)
(:Commit)-[:PART_OF]->(:Branch)
(:Commit)-[:TOUCHES]->(:Component)
*/

CALL db.createRelationshipType('CONTAINS');
CALL db.createRelationshipType('PART_OF');
CALL db.createRelationshipType('TOUCHES');

/*
(:Discussion)-[:MENTIONS]->(:Component)
(:Discussion)-[:CREATES]->(:TrelloCard)
*/

CALL db.createRelationshipType('MENTIONS');
CALL db.createRelationshipType('CREATES');

/*
(:Release)-[:INCLUDES]->(:Commit)
(:Document)-[:DESCRIBES]->(:Project)
(:Document)-[:SUMMARIZES]->(:Release)
*/

CALL db.createRelationshipType('INCLUDES');
CALL db.createRelationshipType('DESCRIBES');
CALL db.createRelationshipType('SUMMARIZES');

/*
(:LLMTask)-[:OUTPUTS]->(:Document)
(:LLMTask)-[:BASED_ON]->(:Discussion)
*/

CALL db.createRelationshipType('OUTPUTS');
CALL db.createRelationshipType('BASED_ON');