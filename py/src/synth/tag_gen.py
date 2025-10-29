import random, uuid
from typing import Dict, Any, List
import numpy as np
from faker import Faker
from .base import EntityGenerator, GeneratorFactory
from .util import get_enum

class TagGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.fake = Faker()
        if seed is not None:
            self.fake.seed_instance(seed)
        self.name_pool = self.cfg.get("names", {}).get("values", [])
        self.type_vals, self.type_w = get_enum(self.cfg, "type", ["THEME","RISK","ESG","STRATEGY"])

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            name = random.choice(self.name_pool) if self.name_pool else self.fake.word().capitalize()
            out.append({
                "id": f"tag-{uuid.uuid4()}",
                "name": name,
                "type": random.choices(self.type_vals, weights=self.type_w, k=1)[0],
            })
        return out

GeneratorFactory.register("tag", TagGenerator)
