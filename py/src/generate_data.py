# src/generate_data.py
from .synth.runner import generate_all

def generate_synthetic_seed():
    entities = [
        "market",
        "sponsor",
        "project",
        "dealterms",
        "investor",           # ya existente
        "investor_mandate",
        "portfolio_position",
        "user_interaction",
        "tag",
    ]
    files = generate_all(
        entities=entities,
        config_dir="/data/config",
        out_dir="/seed/generated",
        fmt="cypher",
        filenames={
            "market": "05-market.cypher",
            "sponsor": "10-sponsor.cypher",
            "project": "15-project.cypher",
            "dealterms": "20-dealterms.cypher",
            "investor": "25-investor.cypher",
            "investor_mandate": "30-investor_mandate.cypher",
            "portfolio_position": "40-portfolio_position.cypher",
            "user_interaction": "50-user_interaction.cypher",
            "tag": "60-tag.cypher",
        },
    )
    print("[synth] Generated:", [str(p) for p in files])

if __name__ == "__main__":
    generate_synthetic_seed()
