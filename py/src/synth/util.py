import yaml, random
from typing import Any, Dict, List, Tuple

def load_yaml(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def choice_weighted(values: List[Any], weights: List[float]) -> Any:
    return random.choices(values, weights=weights, k=1)[0]

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(v, hi))

def get_enum(config: Dict, key: str, fallback: Any) -> Tuple[List[Any], List[float]]:
    enums = config.get("enums", {}).get(key, {})
    values = enums.get("values", fallback if isinstance(fallback, list) else [fallback])
    weights = enums.get("weights", [1.0/len(values)]*len(values))
    return values, weights
