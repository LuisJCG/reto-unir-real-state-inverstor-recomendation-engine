CREATE CONSTRAINT investor_id            IF NOT EXISTS FOR (n:Investor)           REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT investor_mandate_id    IF NOT EXISTS FOR (n:InvestorMandate)    REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT project_id             IF NOT EXISTS FOR (n:Project)            REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT sponsor_id             IF NOT EXISTS FOR (n:Sponsor)            REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT dealterms_id           IF NOT EXISTS FOR (n:DealTerms)          REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT market_id              IF NOT EXISTS FOR (n:Market)             REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT tag_id                 IF NOT EXISTS FOR (n:Tag)                REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT pos_id                 IF NOT EXISTS FOR (n:PortfolioPosition)  REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT ui_id                  IF NOT EXISTS FOR (n:UserInteraction)    REQUIRE n.id IS UNIQUE;

MERGE (m1:Market {id:"Madrid-ES"})
SET  m1.city="Madrid",
     m1.country="ES",
     m1.vacancy_rate=0.06,
     m1.rent_growth=0.03,
     m1.cap_rate_market=0.045;

MERGE (sp1:Sponsor {id:"sp1"})
SET  sp1.name="IberoCapital",
     sp1.reputation_score=0.8,
     sp1.track_record_irr_avg=0.14,
     sp1.deals_count=25,
     sp1.focus_geos=["ES"],
     sp1.focus_asset_types=["Residential","Logistics"];

MERGE (tESG:Tag  {id:"tag-esg-high"}) SET tESG.name="ESG-High", tESG.type="ESG";
MERGE (tCore:Tag {id:"tag-core"})     SET tCore.name="Core",     tCore.type="Strategy";

MERGE (p1:Project {id:"proj-1"})
SET  p1.name="Madrid Resi Dev A",
     p1.asset_type="Residential",
     p1.stage="Development",
     p1.city="Madrid", p1.country="ES",
     p1.lat=40.4168, p1.lon=-3.7038,
     p1.irr_est=0.18, p1.yield_est=0.0,
     p1.ltv=0.55, p1.risk_score=0.35, p1.esg_score=0.7,
     p1.min_ticket=500000, p1.horizon="MID",
     p1.currency="EUR", p1.text_desc="Infill resi development in Madrid";

MERGE (p2:Project {id:"proj-2"})
SET  p2.name="Madrid Logistics B",
     p2.asset_type="Logistics",
     p2.stage="Core",
     p2.city="Madrid", p2.country="ES",
     p2.lat=40.4, p2.lon=-3.7,
     p2.irr_est=0.11, p2.yield_est=0.06,
     p2.ltv=0.45, p2.risk_score=0.25, p2.esg_score=0.8,
     p2.min_ticket=300000, p2.horizon="LONG",
     p2.currency="EUR", p2.text_desc="Stabilized logistics asset";

MERGE (dt1:DealTerms {id:"terms-1"})
SET  dt1.structure="Equity",
     dt1.preferred_return_pct=0.08,
     dt1.management_fee_pct=0.02,
     dt1.performance_fee_pct=0.20,
     dt1.lockup_months=24,
     dt1.distribution_policy="quarterly";
MERGE (p1)-[:HAS_TERMS]->(dt1);

MERGE (i1:Investor {id:"inv-1"})
SET  i1.segment="FamilyOffice",
     i1.risk_profile="Balanced",
     i1.horizon="MID",
     i1.ticket_min=200000,
     i1.ticket_max=1500000,
     i1.jurisdictions_ok=["ES"],
     i1.esg_pref=0.6,
     i1.created_at = coalesce(i1.created_at, datetime());

MERGE (im1:InvestorMandate {id:"mand-1"})
SET  im1.asset_types_allowed=["Residential","Logistics"],
     im1.stages_allowed=["Core","Development"],
     im1.geographies_allowed=["ES"],
     im1.min_target_irr=0.10,
     im1.max_ltv=0.6,
     im1.min_esg_score=0.5,
     im1.ticket_min=250000,
     im1.ticket_max=1200000,
     im1.effective_from=date(),
     im1.effective_to = date() + duration({years:3});

MERGE (p1)-[:SPONSORED_BY]->(sp1);
MERGE (p2)-[:SPONSORED_BY]->(sp1);
MERGE (p1)-[:LOCATED_IN]->(m1);
MERGE (p2)-[:LOCATED_IN]->(m1);
MERGE (p1)-[:HAS_TAG]->(tESG);
MERGE (p2)-[:HAS_TAG]->(tCore);
MERGE (i1)-[:HAS_MANDATE]->(im1);
MERGE (i1)-[:PREFERS]->(tESG);


MERGE (ui1:UserInteraction {id:"ui-1"})
SET  ui1.type="VIEW",
     ui1.ts = coalesce(ui1.ts, datetime()),
     ui1.weight=0.3;
MERGE (i1)-[:INTERACTED]->(ui1);
MERGE (ui1)-[:ON]->(p2);


MERGE (pos1:PortfolioPosition {id:"pos-1"})
SET  pos1.committed_amount=300000,
     pos1.entry_date=date() - duration({months:18}),
     pos1.exit_date=null,
     pos1.status="Active",
     pos1.currency="EUR";
MERGE (pos1)-[:IN]->(p2);
MERGE (i1)-[:HELD]->(pos1);
