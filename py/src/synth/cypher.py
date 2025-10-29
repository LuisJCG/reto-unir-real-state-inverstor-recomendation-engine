from typing import Any, Dict

def _esc(s: str) -> str:
    return s.replace("\\", "\\\\").replace("'", "\\'")

def _fmt(v: Any) -> str:
    if v is None:
        return "null"
    if isinstance(v, bool):
        return "true" if v else "false"
    if isinstance(v, (int, float)):
        return str(v)
    if isinstance(v, list):
        return "[" + ", ".join(_fmt(x) for x in v) + "]"
    return f"'{_esc(str(v))}'"

def investor_to_cypher(p: Dict[str, Any]) -> str:
    if "id" not in p:
        raise ValueError("Investor requires 'id'")
    props_order = [
        "name",
        "investor_type",
        "city",
        "country",
        "aum",
        "ticket_min",
        "ticket_max",
        "currency",
        "min_target_irr",
        "max_ltv",
        "min_esg_score",
        "risk_appetite",
        "focus_geos",
        "focus_asset_types",
        "tags",
        "website",
        "email",
    ]
    sets = []
    for k in props_order:
        if k in p:
            sets.append(f"n.{k}={_fmt(p[k])}")
    set_clause = ", ".join(sets) if sets else ""
    if set_clause:
        return f"MERGE (n:Investor {{id:'{_esc(str(p['id']))}'}}) SET {set_clause};"
    else:
        return f"MERGE (n:Investor {{id:'{_esc(str(p['id']))}'}});"

def project_to_cypher(p: Dict) -> str:
    return (
        "MERGE (n:Project {id:'%s'}) SET "
        "n.name='%s', n.asset_type='%s', n.stage='%s', "
        "n.city='%s', n.country='%s', n.lat=%s, n.lon=%s, "
        "n.irr_est=%s, n.yield_est=%s, n.ltv=%s, "
        "n.risk_score=%s, n.esg_score=%s, n.min_ticket=%s, "
        "n.horizon='%s', n.currency='%s', n.text_desc='%s';"
    ) % (
        _esc(p["id"]), _esc(p["name"]), _esc(p["asset_type"]), _esc(p["stage"]),
        _esc(p["city"]), _esc(p["country"]), p["lat"], p["lon"],
        p["irr_est"], p["yield_est"], p["ltv"],
        p["risk_score"], p["esg_score"], p["min_ticket"],
        _esc(p["horizon"]), _esc(p["currency"]), _esc(p["text_desc"]),
    )

def investor_mandate_to_cypher(m: Dict) -> str:
    return (
        "MERGE (n:InvestorMandate {id:'%s'}) SET "
        "n.asset_types_allowed=%s, n.stages_allowed=%s, n.geographies_allowed=%s, "
        "n.min_target_irr=%s, n.max_ltv=%s, n.min_esg_score=%s, "
        "n.ticket_min=%s, n.ticket_max=%s, "
        "n.effective_from=date('%s'), n.effective_to=date('%s');"
    ) % (
        _esc(m["id"]),
        str(m["asset_types_allowed"]), str(m["stages_allowed"]), str(m["geographies_allowed"]),
        m["min_target_irr"], m["max_ltv"], m["min_esg_score"],
        m["ticket_min"], m["ticket_max"],
        _esc(m["effective_from"]), _esc(m["effective_to"])
    )

def sponsor_to_cypher(s: Dict) -> str:
    return (
        "MERGE (n:Sponsor {id:'%s'}) SET "
        "n.name='%s', n.reputation_score=%s, n.track_record_irr_avg=%s, n.deals_count=%s, "
        "n.focus_geos=%s, n.focus_asset_types=%s;"
    ) % (
        _esc(s["id"]), _esc(s["name"]), s["reputation_score"], s["track_record_irr_avg"],
        s["deals_count"], str(s["focus_geos"]), str(s["focus_asset_types"])
    )

def dealterms_to_cypher(d: Dict) -> str:
    return (
        "MERGE (n:DealTerms {id:'%s'}) SET "
        "n.structure='%s', n.preferred_return_pct=%s, n.management_fee_pct=%s, "
        "n.performance_fee_pct=%s, n.lockup_months=%s, n.distribution_policy='%s';"
    ) % (
        _esc(d["id"]), _esc(d["structure"]), d["preferred_return_pct"],
        d["management_fee_pct"], d["performance_fee_pct"],
        d["lockup_months"], _esc(d["distribution_policy"])
    )

def market_to_cypher(m: Dict) -> str:
    return (
        "MERGE (n:Market {id:'%s'}) SET "
        "n.city='%s', n.country='%s', n.vacancy_rate=%s, n.rent_growth=%s, n.cap_rate_market=%s;"
    ) % (
        _esc(m["id"]), _esc(m["city"]), _esc(m["country"]),
        m["vacancy_rate"], m["rent_growth"], m["cap_rate_market"]
    )

def portfolio_position_to_cypher(p: Dict) -> str:
    return (
        "MERGE (n:PortfolioPosition {id:'%s'}) SET "
        "n.committed_amount=%s, n.entry_date=date('%s'), "
        "n.exit_date=%s, n.status='%s', n.currency='%s';"
    ) % (
        _esc(p["id"]), p["committed_amount"], _esc(p["entry_date"]),
        ("date('%s')" % _esc(p["exit_date"])) if p.get("exit_date") else "null",
        _esc(p["status"]), _esc(p["currency"])
    )

def user_interaction_to_cypher(u: Dict) -> str:
    return (
        "MERGE (n:UserInteraction {id:'%s'}) SET "
        "n.type='%s', n.ts=datetime('%s'), n.weight=%s;"
    ) % (
        _esc(u["id"]), _esc(u["type"]), _esc(u["ts"]), u["weight"]
    )

def tag_to_cypher(t: Dict) -> str:
    return (
        "MERGE (n:Tag {id:'%s'}) SET "
        "n.name='%s', n.type='%s';"
    ) % (_esc(t["id"]), _esc(t["name"]), _esc(t["type"]))
