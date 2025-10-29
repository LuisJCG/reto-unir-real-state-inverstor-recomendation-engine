import random, uuid, datetime
from typing import Dict, Any, List
import numpy as np
from .base import EntityGenerator, GeneratorFactory
from .util import get_enum

class UserInteractionGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed); np.random.seed(seed)
        self.type_vals, self.type_w = get_enum(self.cfg, "type", ["VIEW","LIKE","BOOKMARK","DISMISS"])

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        now = datetime.datetime.utcnow()
        for _ in range(n):
            dt = now - datetime.timedelta(days=random.randint(0, 90), seconds=random.randint(0, 86400))
            out.append({
                "id": f"ui-{uuid.uuid4()}",
                "type": random.choices(self.type_vals, weights=self.type_w, k=1)[0],
                "ts": dt.replace(microsecond=0).isoformat() + "Z",
                "weight": round(random.uniform(0.1, 1.0), 5),
            })
        return out

GeneratorFactory.register("user_interaction", UserInteractionGenerator)
