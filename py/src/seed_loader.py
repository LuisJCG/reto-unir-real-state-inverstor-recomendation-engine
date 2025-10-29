from neo4j import GraphDatabase
from pathlib import Path
import os
from .config import NEO4J_BOLT, NEO4J_USER, NEO4J_PASSWORD

# If SEED_PATH is a directory, load all *.cypher (recursively), sorted.
SEED_PATH = os.getenv("SEED_PATH", "/seed")

def _iter_statements_from_file(path: Path):
    cypher = path.read_text(encoding="utf-8")
    for stmt in [x.strip() for x in cypher.split(";") if x.strip()]:
        yield stmt

def _iter_statements(seed_path: Path):
    if seed_path.is_file():
        yield from _iter_statements_from_file(seed_path)
    elif seed_path.is_dir():
        for f in sorted(seed_path.rglob("*.cypher")):
            for stmt in _iter_statements_from_file(f):
                yield stmt
    else:
        raise FileNotFoundError(f"SEED_PATH not found: {seed_path}")

def run_seed():
    driver = GraphDatabase.driver(NEO4J_BOLT, auth=(NEO4J_USER, NEO4J_PASSWORD))
    seed_path = Path(SEED_PATH)
    count = 0
    with driver.session() as s:
        for stmt in _iter_statements(seed_path):
            s.run(stmt)
            count += 1
    driver.close()
    print(f"Seed completed. Executed {count} statements from {seed_path}")

if __name__ == "__main__":
    run_seed()
