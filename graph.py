from wiki import get_all_links
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
DATABASE = "wikirace"
driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

def get_unexplored():
    records = driver.execute_query("""
            MATCH (a: Article {explored: FALSE}) 
            RETURN a.name AS name
            """,
        database_ = DATABASE,
    ).records
    
    return [record.data()["name"] for record in records]

def create_article(parent, child):
    driver.execute_query("""
        MATCH (p:Article {name: $parent})
        MERGE (c:Article {name: $child})
        ON CREATE SET c.explored = FALSE
        MERGE (p)-[:parent_of]->(c)
        """,
        parent=parent,
        child=child,
        database_=DATABASE,
    )

def update_explored(name):
    driver.execute_query("""
        MATCH (a:Article {name: $name})
        SET a.explored = TRUE
        """,
        name=name,
        database_=DATABASE,
    )

def main():
    print("[LOG] Checking unexplored")

    unexplored = get_unexplored()

    print(f"[LOG] {len(unexplored)} items to explore")

    if len(unexplored) == 0:
        print("[LOG] Terminating program, no more to explore")
        return
    
    for name in unexplored:
        print(f"[LOG] Exploring {name}")
        links = get_all_links(name)

        for link in links:
            create_article(name, link)

        update_explored(name)
    
    main()
        
main()