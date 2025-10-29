from neo4j import GraphDatabase
from .config import NEO4J_BOLT, NEO4J_USER, NEO4J_PASSWORD

def run():
    driver = GraphDatabase.driver(NEO4J_BOLT, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session(database="neo4j") as s:
        s.run("CALL gds.graph.drop('gw', false) YIELD graphName").consume()

        s.run("""
        CALL gds.graph.project.cypher(
          'gw',
          $nodeQuery,
          $relQuery,
          { validateRelationships: false }   // ignora las rels cuyos extremos no estén proyectados
        )
        """, {
          "nodeQuery": """
            MATCH (n)
            WHERE n:Investor OR n:Project OR n:Tag OR n:Sponsor OR n:Market
            RETURN id(n) AS id, labels(n) AS labels
          """,
          "relQuery": """
            MATCH (a)-[r:SPONSORED_BY|LOCATED_IN|HAS_TAG|PREFERS]->(b)
            WHERE (
              (a:Investor OR a:Project OR a:Tag OR a:Sponsor OR a:Market) AND
              (b:Investor OR b:Project OR b:Tag OR b:Sponsor OR b:Market)
            )
            RETURN id(a) AS source, id(b) AS target, type(r) AS type
          """
        }).consume()


        res = s.run("""
        CALL gds.fastRP.mutate('gw', {
          embeddingDimension: 64,
          mutateProperty: 'embedding'
        })
        YIELD nodeCount, mutateMillis
        """).single()
        print(f"[GDS] FastRP: nodes={res['nodeCount']}, mutate_ms={res['mutateMillis']}")

        sim = s.run("""
        CALL gds.knn.write('gw', {
          nodeLabels: ['Investor','Project'],
          nodeProperties: ['embedding'],
          topK: 10,
          sampleRate: 1.0,
          similarityCutoff: 0.0,
          concurrency: 2,
          writeRelationshipType: 'SIMILAR_TO',
          writeProperty: 'score'
        })
        YIELD nodesCompared, relationshipsWritten
        RETURN nodesCompared, relationshipsWritten
        """).single()
        print(f"[GDS] KNN: compared={sim['nodesCompared']}, written={sim['relationshipsWritten']}")


    driver.close()

if __name__ == "__main__":
    run()
