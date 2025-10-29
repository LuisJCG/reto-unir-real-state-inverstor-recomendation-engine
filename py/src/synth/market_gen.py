import random, uuid
from typing import Dict, Any, List
import numpy as np
from faker import Faker
from .base import EntityGenerator, GeneratorFactory

class MarketGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.fake = Faker()
        if seed is not None:
            self.fake.seed_instance(seed)
        self.defs = self.cfg.get("defaults", {})

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            city = self.fake.city()
            country = self.fake.country_code(representation="alpha-2")
            out.append({
                "id": f"{city}-{country}".replace(" ", "_"),
                "city": city,
                "country": country,
                "vacancy_rate": round(random.uniform(*self.defs.get("vacancy_rate_range",[0.02,0.20])),5),
                "rent_growth": round(random.uniform(*self.defs.get("rent_growth_range",[-0.03,0.10])),5),
                "cap_rate_market": round(random.uniform(*self.defs.get("cap_rate_market_range",[0.03,0.08])),5),
            })
        return out

GeneratorFactory.register("market", MarketGenerator)
