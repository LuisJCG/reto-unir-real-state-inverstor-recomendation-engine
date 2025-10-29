import random, uuid
from typing import Dict, Any, List
import numpy as np
from .base import EntityGenerator, GeneratorFactory
from .util import get_enum

class DealTermsGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.defs = self.cfg.get("defaults", {})
        self.struct_vals, self.struct_w = get_enum(self.cfg, "structure", ["closed_end_fund","spv","club_deal"])
        self.dist_vals, self.dist_w = get_enum(self.cfg, "distribution_policy", ["quarterly","semiannual","annual"])

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            out.append({
                "id": f"terms-{uuid.uuid4()}",
                "structure": random.choices(self.struct_vals, weights=self.struct_w, k=1)[0],
                "preferred_return_pct": round(random.uniform(*self.defs.get("preferred_return_pct_range",[0.06,0.12])),5),
                "management_fee_pct": round(random.uniform(*self.defs.get("management_fee_pct_range",[0.005,0.02])),5),
                "performance_fee_pct": round(random.uniform(*self.defs.get("performance_fee_pct_range",[0.1,0.25])),5),
                "lockup_months": int(random.uniform(*self.defs.get("lockup_months_range",[12,72]))),
                "distribution_policy": random.choices(self.dist_vals, weights=self.dist_w, k=1)[0],
            })
        return out

GeneratorFactory.register("dealterms", DealTermsGenerator)
