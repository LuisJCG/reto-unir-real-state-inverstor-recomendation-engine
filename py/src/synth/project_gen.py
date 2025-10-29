import random, uuid
from typing import Dict, Any, List
from faker import Faker
import numpy as np

from .base import EntityGenerator, GeneratorFactory
from .util import choice_weighted, clamp, get_enum

class ProjectGenerator(EntityGenerator):
    def __init__(self, config: Dict[str, Any]):
        self.cfg = config or {}
        seed = self.cfg.get("random_seed")
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.fake = Faker()
        if seed is not None:
            self.fake.seed_instance(seed)

        self.defs = self.cfg.get("defaults", {})
        self.countries = self.cfg.get("countries", {}).get("include", None)
        names = self.cfg.get("names", {}) or {}
        self.name_prefix = names.get("prefix", ["Prime", "Urban", "Green"])
        self.name_suffix = names.get("suffix", ["Hub", "Plaza", "Tower"])
        self.free_text_sentences = int(self.cfg.get("free_text", {}).get("sentences", 2))

        self.asset_type_vals, self.asset_type_w = get_enum(
            self.cfg, "asset_type", ["residential", "office", "logistics"]
        )
        self.stage_vals, self.stage_w = get_enum(
            self.cfg, "stage", ["development", "value_add", "core_plus", "core"]
        )
        self.horizon_vals, self.horizon_w = get_enum(
            self.cfg, "horizon", ["mid"]
        )
        self.currency_vals, self.currency_w = get_enum(
            self.cfg, "currency", ["EUR"]
        )

    def _rand_range(self, key: str, default_lo: float, default_hi: float) -> float:
        lo, hi = self.defs.get(f"{key}_range", [default_lo, default_hi])
        return random.uniform(lo, hi)

    def _pick_country_city(self) -> Dict[str, str]:
        country = random.choice(self.countries) if self.countries else self.fake.country_code(representation="alpha-2")
        return {"country": country, "city": self.fake.city()}

    def _name(self) -> str:
        return f"{random.choice(self.name_prefix)} {random.choice(self.name_suffix)}"

    def _text(self) -> str:
        return " ".join(self.fake.sentences(self.free_text_sentences))

    def _finance_block(self) -> Dict[str, float]:
        irr = self._rand_range("irr_est", 0.06, 0.20)
        yld = self._rand_range("yield_est", 0.03, 0.10)
        ltv = self._rand_range("ltv", 0.35, 0.70)
        esg = self._rand_range("esg_score", 0.25, 0.90)
        raw_risk = 0.5 * (ltv) + 0.5 * (1.0 - (irr - 0.05) / (0.25 - 0.05))
        risk = clamp(raw_risk, *self.defs.get("risk_score_range", [0.1, 0.85]))
        ticket = self._rand_range("min_ticket", 250_000, 5_000_000)
        return {
            "irr_est": round(irr, 5),
            "yield_est": round(yld, 5),
            "ltv": round(ltv, 5),
            "risk_score": round(risk, 5),
            "esg_score": round(esg, 5),
            "min_ticket": round(ticket),
        }

    def generate(self, n: int) -> List[Dict[str, Any]]:
        out = []
        for _ in range(n):
            enums = {
                "asset_type": choice_weighted(self.asset_type_vals, self.asset_type_w),
                "stage": choice_weighted(self.stage_vals, self.stage_w),
                "horizon": choice_weighted(self.horizon_vals, self.horizon_w),
                "currency": choice_weighted(self.currency_vals, self.currency_w),
            }
            cc = self._pick_country_city()
            fin = self._finance_block()
            out.append({
                "id": f"proj-{uuid.uuid4()}",
                "name": self._name(),
                "asset_type": enums["asset_type"],
                "stage": enums["stage"],
                "city": cc["city"],
                "country": cc["country"],
                "lat": self._rand_range("lat", -90.0, 90.0),
                "lon": self._rand_range("lon", -180.0, 180.0),
                "irr_est": fin["irr_est"],
                "yield_est": fin["yield_est"],
                "ltv": fin["ltv"],
                "risk_score": fin["risk_score"],
                "esg_score": fin["esg_score"],
                "min_ticket": fin["min_ticket"],
                "horizon": enums["horizon"],
                "currency": enums["currency"],
                "text_desc": self._text(),
            })
        return out


GeneratorFactory.register("project", ProjectGenerator)
