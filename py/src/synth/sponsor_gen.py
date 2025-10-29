import random, uuid
from typing import Dict, Any, List
import numpy as np
from faker import Faker
from .base import EntityGenerator, GeneratorFactory

class SponsorGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.fake = Faker()
        if seed is not None:
            self.fake.seed_instance(seed)
        self.defs = self.cfg.get("defaults", {})
        self.geos = self.cfg.get("geographies", {}).get("values", ["ES","FR","DE","IT","UK","NL"])
        self.asset_types = self.cfg.get("asset_types", {}).get("values", ["residential","office","retail","logistics"])

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            out.append({
                "id": f"spon-{uuid.uuid4()}",
                "name": self.fake.company(),
                "reputation_score": round(random.uniform(*self.defs.get("reputation_score_range",[0.3,0.95])),5),
                "track_record_irr_avg": round(random.uniform(*self.defs.get("track_record_irr_avg_range",[0.07,0.22])),5),
                "deals_count": int(random.uniform(*self.defs.get("deals_count_range",[3,120]))),
                "focus_geos": random.sample(self.geos, k=random.randint(1, min(5, len(self.geos)))),
                "focus_asset_types": random.sample(self.asset_types, k=random.randint(1, min(3, len(self.asset_types)))),
            })
        return out

GeneratorFactory.register("sponsor", SponsorGenerator)
