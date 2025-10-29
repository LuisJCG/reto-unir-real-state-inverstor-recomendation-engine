import random, uuid, datetime
from typing import Dict, Any, List
import numpy as np
from .base import EntityGenerator, GeneratorFactory
from .util import get_enum

class PortfolioPositionGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.defs = self.cfg.get("defaults", {})
        self.status_vals, self.status_w = get_enum(self.cfg, "status", ["OPEN","CLOSED","PENDING"])
        self.curr_vals, self.curr_w = get_enum(self.cfg, "currency", ["EUR","USD","GBP"])

    def _rand_dates(self):
        start = datetime.date.today() - datetime.timedelta(days=365*5)
        entry = start + datetime.timedelta(days=random.randint(0, 365*5))
        if random.random() < 0.6:
            exit_d = None
        else:
            exit_d = entry + datetime.timedelta(days=random.randint(90, 365*4))
        return entry.isoformat(), (exit_d.isoformat() if exit_d else None)

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            entry, exit_d = self._rand_dates()
            out.append({
                "id": f"pp-{uuid.uuid4()}",
                "committed_amount": round(random.uniform(*self.defs.get("committed_amount_range",[250_000, 10_000_000]))),
                "entry_date": entry,
                "exit_date": exit_d,
                "status": random.choices(self.status_vals, weights=self.status_w, k=1)[0],
                "currency": random.choices(self.curr_vals, weights=self.curr_w, k=1)[0],
            })
        return out

GeneratorFactory.register("portfolio_position", PortfolioPositionGenerator)
