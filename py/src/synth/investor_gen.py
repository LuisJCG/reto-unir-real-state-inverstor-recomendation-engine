import random, uuid
from typing import Dict, Any, List
from faker import Faker
import numpy as np

from .base import EntityGenerator, GeneratorFactory
from .util import choice_weighted

class InvestorGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.fake = Faker()
        if seed is not None: self.fake.seed_instance(seed)

        self.defs = self.cfg.get("defaults", {})
        enums = self.cfg.get("enums", {})
        self.segment_vals = enums.get("segment", {}).get("values", ["retail"])
        self.segment_w    = enums.get("segment", {}).get("weights", [1.0])
        self.risk_vals    = enums.get("risk_profile", {}).get("values", ["medium"])
        self.risk_w       = enums.get("risk_profile", {}).get("weights", [1.0])
        self.horizon_vals = enums.get("horizon", {}).get("values", ["mid"])
        self.horizon_w    = enums.get("horizon", {}).get("weights", [1.0])

        self.jurisdictions = self.cfg.get("jurisdictions", {}).get("include", ["US"])

    def _rand_range(self, key: str, default_lo: float, default_hi: float) -> float:
        lo, hi = self.defs.get(f"{key}_range", [default_lo, default_hi])
        return random.uniform(lo, hi)

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            inv_id = f"inv-{uuid.uuid4()}"
            ticket_min = round(self._rand_range("ticket_min", 100000, 1000000))
            ticket_max = round(self._rand_range("ticket_max", 2000000, 20000000))
            if ticket_max < ticket_min:
                ticket_max, ticket_min = ticket_min, ticket_max

            out.append({
                "id": inv_id,
                "segment": choice_weighted(self.segment_vals, self.segment_w),
                "risk_profile": choice_weighted(self.risk_vals, self.risk_w),
                "horizon": choice_weighted(self.horizon_vals, self.horizon_w),
                "ticket_min": ticket_min,
                "ticket_max": ticket_max,
                "jurisdictions_ok": random.sample(self.jurisdictions, k=random.randint(1, min(3, len(self.jurisdictions)))),
                "esg_pref": round(self._rand_range("esg_pref", 0.0, 1.0), 3),
                "created_at": self.fake.date_time_this_decade().isoformat(),
            })
        return out

# register
GeneratorFactory.register("investor", InvestorGenerator)
