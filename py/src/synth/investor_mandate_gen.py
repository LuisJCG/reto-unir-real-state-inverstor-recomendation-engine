import random, uuid, datetime
from typing import Dict, Any, List
import numpy as np
from .base import EntityGenerator, GeneratorFactory
from .util import choice_weighted, get_enum

class InvestorMandateGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.defs = self.cfg.get("defaults", {})

        self.asset_vals, self.asset_w = get_enum(self.cfg, "asset_type", ["residential","office","logistics"])
        self.stage_vals, self.stage_w = get_enum(self.cfg, "stage", ["development","value_add","core_plus","core"])
        self.geo_vals = self.cfg.get("geographies", {}).get("values", ["ES","FR","DE","IT","UK"])

        self.irr_range = self.defs.get("min_target_irr_range", [0.06, 0.20])
        self.ltv_max_range = self.defs.get("max_ltv_range", [0.4, 0.75])
        self.esg_min_range = self.defs.get("min_esg_score_range", [0.2, 0.9])
        self.tmin_range = self.defs.get("ticket_min_range", [250_000, 5_000_000])
        self.tmax_factor = self.defs.get("ticket_max_factor", [1.5, 5.0])
        self.window_years = int(self.defs.get("effective_window_years", 3))

    def _rand_date(self) -> (str, str):
        start = datetime.date.today() - datetime.timedelta(days=365*self.window_years)
        end = datetime.date.today() + datetime.timedelta(days=365*self.window_years)
        d1 = start + datetime.timedelta(days=random.randint(0, (end-start).days//2))
        d2 = d1 + datetime.timedelta(days=random.randint(30, 365*2))
        return d1.isoformat(), d2.isoformat()

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            min_irr = round(random.uniform(*self.irr_range), 5)
            max_ltv = round(random.uniform(*self.ltv_max_range), 5)
            min_esg = round(random.uniform(*self.esg_min_range), 5)
            tmin = round(random.uniform(*self.tmin_range))
            tmax = round(tmin * random.uniform(*self.tmax_factor))
            eff_from, eff_to = self._rand_date()
            # multi-selects
            assets = list({choice_weighted(self.asset_vals, self.asset_w) for _ in range(random.randint(1, min(3, len(self.asset_vals))))})
            stages = list({choice_weighted(self.stage_vals, self.stage_w) for _ in range(random.randint(1, min(3, len(self.stage_vals))))})
            geos = random.sample(self.geo_vals, k=random.randint(1, min(5, len(self.geo_vals))))
            out.append({
                "id": f"mand-{uuid.uuid4()}",
                "asset_types_allowed": assets,
                "stages_allowed": stages,
                "geographies_allowed": geos,
                "min_target_irr": min_irr,
                "max_ltv": max_ltv,
                "min_esg_score": min_esg,
                "ticket_min": tmin,
                "ticket_max": tmax,
                "effective_from": eff_from,
                "effective_to": eff_to
            })
        return out

GeneratorFactory.register("investor_mandate", InvestorMandateGenerator)
