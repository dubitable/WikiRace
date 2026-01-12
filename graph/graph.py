from wiki import get_all_links
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

load_dotenv()

URI = os.getenv("NEO4J_URI")
AUTH = (os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
DATABASE = "wikirace"

def get_unexplored(driver):
    records = driver.execute_query("""
            MATCH (a: Article {explored: FALSE}) 
            RETURN a.name AS name
            """,
        database_ = DATABASE,
    ).records
    
    return [record.data()["name"] for record in records]

def create_article(driver, parent, child):
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

def update_explored(driver, name):
    driver.execute_query("""
        MATCH (a:Article {name: $name})
        SET a.explored = TRUE
        """,
        name=name,
        database_=DATABASE,
    )

out_bounds = ["Talk", "User", "Wikipedia", "File", "MediaWiki", "Template", "Help", "Category", "Portal", "Draft", "MOS", "TimedText", "Module", "Event",
              "Book", "Course", "Institution", "Education Program", "Gadget", "Gadget definition", "Topic",
              "Special", "Media"]

def is_out_bounds(name):
    for out_bound in out_bounds:
        if name.startswith(out_bound + ":") or name.startswith(out_bound + " talk:"):
            return True
    return False

def main(driver):
    print("[LOG] Checking unexplored")

    unexplored = get_unexplored(driver)

    print(f"[LOG] {len(unexplored)} items to explore")

    if len(unexplored) == 0:
        print("[LOG] Terminating program, no more to explore")
        return
    
    for name in unexplored:
        print(f"[LOG] Exploring {name}")
        links = get_all_links(name)

        for link in links:
            if (is_out_bounds(link)): continue
            create_article(driver, name, link)

        update_explored(driver, name)
    
    main(driver)

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    main(driver)