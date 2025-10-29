from neo4j import GraphDatabase
from .config import NEO4J_BOLT, NEO4J_USER, NEO4J_PASSWORD

def _score_feat(p, mandate, inv):
    s = 0.0
    if p.get("irr_est") is not None and mandate.get("min_target_irr") is not None:
        if p["irr_est"] >= mandate["min_target_irr"]:
            s += 0.4
    if p.get("ltv") is not None and mandate.get("max_ltv") is not None:
        if p["ltv"] <= mandate["max_ltv"]:
            s += 0.3
    if p.get("esg_score") is not None and mandate.get("min_esg_score") is not None:
        s += 0.2 * (1.0 if p["esg_score"] >= mandate["min_esg_score"] else 0.0)
    if p.get("min_ticket") is not None and inv.get("ticket_min") is not None and inv.get("ticket_max") is not None:
        if inv["ticket_min"] <= p["min_ticket"] <= inv["ticket_max"]:
            s += 0.1
    return s

def _query_candidates(session, inv_id: str):
    q = """
    MATCH (i:Investor {id:$inv_id})
    OPTIONAL MATCH (i)-[:HAS_MANDATE]->(m:InvestorMandate)
    WITH i, m
    MATCH (p:Project)
    WHERE
      // Si NO hay mandato, no filtra por él. Si lo hay, aplica filtros.
      (m IS NULL OR (
        (m.geographies_allowed IS NULL OR p.country IN m.geographies_allowed) AND
        (m.asset_types_allowed IS NULL OR p.asset_type IN m.asset_types_allowed) AND
        (m.stages_allowed      IS NULL OR p.stage      IN m.stages_allowed)      AND
        coalesce(p.ltv, 1.0)      <= coalesce(m.max_ltv, 1.0)                    AND
        coalesce(p.esg_score,0.0) >= coalesce(m.min_esg_score, 0.0)              AND
        (m.ticket_min IS NULL OR coalesce(p.min_ticket, 9e18) >= m.ticket_min)   AND
        (m.ticket_max IS NULL OR coalesce(p.min_ticket, 0)    <= m.ticket_max)
      ))
    OPTIONAL MATCH (i)-[sim:SIMILAR_TO]-(p)   // no dirigido
    RETURN i{.*} AS investor, coalesce(m{.*},{}) AS mandate, p{.*} AS project, coalesce(sim.score, 0.0) AS simScore
    """
    return session.run(q, {"inv_id": inv_id}).data()

def topn_for_investor(inv_id: str, n: int = 10):
    driver = GraphDatabase.driver(NEO4J_BOLT, auth=(NEO4J_USER, NEO4J_PASSWORD))
    with driver.session(database="neo4j") as s:
        rows = _query_candidates(s, inv_id)
        if not rows:
            return []  

        investor = rows[0]["investor"]
        mandate  = rows[0]["mandate"]

        scored = []
        for row in rows:
            p   = row["project"]
            sim = row["simScore"]
            feat = _score_feat(p, mandate, investor)
            final = 0.7 * sim + 0.3 * feat
            scored.append({
                "project_id": p.get("id"),
                "name": p.get("name"),
                "country": p.get("country"),
                "asset_type": p.get("asset_type"),
                "stage": p.get("stage"),
                "irr_est": p.get("irr_est"),
                "ltv": p.get("ltv"),
                "esg_score": p.get("esg_score"),
                "min_ticket": p.get("min_ticket"),
                "similarity": sim,
                "feat_score": feat,
                "final_score": round(final, 6),
            })

        scored.sort(key=lambda x: x["final_score"], reverse=True)
        return scored[:n]

if __name__ == "__main__":
    import argparse, json
    parser = argparse.ArgumentParser()
    parser.add_argument("--inv", default="inv-1")
    parser.add_argument("--n", type=int, default=5)
    args = parser.parse_args()
    out = topn_for_investor(args.inv, n=args.n)
    print(json.dumps(out, indent=2, ensure_ascii=False))
