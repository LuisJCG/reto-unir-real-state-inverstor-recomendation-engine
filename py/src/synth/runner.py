# src/synth/runner.py
from pathlib import Path
from typing import Iterable, List, Dict, Any, Optional
import json, importlib
from .base import GeneratorFactory
from .util import load_yaml
from .cypher import (
    project_to_cypher,
    investor_mandate_to_cypher,
    sponsor_to_cypher,
    dealterms_to_cypher,
    market_to_cypher,
    portfolio_position_to_cypher,
    user_interaction_to_cypher,
    tag_to_cypher,
    investor_to_cypher
)

_SERIALIZERS = {
    "investor": investor_to_cypher,
    "project": project_to_cypher,
    "investor_mandate": investor_mandate_to_cypher,
    "sponsor": sponsor_to_cypher,
    "dealterms": dealterms_to_cypher,
    "market": market_to_cypher,
    "portfolio_position": portfolio_position_to_cypher,
    "user_interaction": user_interaction_to_cypher,
    "tag": tag_to_cypher,
}

def _write(entity: str, rows: List[Dict[str, Any]], out_dir: Path, fmt: str = "cypher", filename: Optional[str] = None) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    fname = filename or (f"{entity}.cypher" if fmt == "cypher" else f"{entity}.json")
    out_path = out_dir / fname
    if fmt == "json":
        out_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False), encoding="utf-8")
    elif fmt == "cypher":
        ser = _SERIALIZERS[entity]
        out_path.write_text("\n".join(ser(r) for r in rows) + "\n", encoding="utf-8")
    else:
        raise ValueError("fmt must be 'cypher' or 'json'")
    return out_path

def _ensure_module_loaded(entity: str) -> None:
    importlib.import_module(f".{entity}_gen", package="src.synth")

def _gen_one(entity: str, config_path: Path, n_override: Optional[int] = None) -> List[Dict[str, Any]]:
    cfg = load_yaml(str(config_path))
    n = int(n_override) if n_override is not None else int(cfg.get("count", 100))
    _ensure_module_loaded(entity)
    gen = GeneratorFactory.create(entity, config=cfg)
    return gen.generate(n)

def generate_all(entities: Iterable[str],
                 config_dir: str = "/data/config",
                 out_dir: str = "/seed/generated",
                 fmt: str = "cypher",
                 n_override: Optional[int] = None,
                 filenames: Optional[Dict[str, str]] = None) -> List[Path]:
    out_paths: List[Path] = []
    cfg_dir = Path(config_dir)
    outp = Path(out_dir)
    names = filenames or {}
    for e in entities:
        cfg_file = cfg_dir / f"{e}.yaml"
        rows = _gen_one(e, cfg_file, n_override=n_override)
        out_paths.append(_write(e, rows, outp, fmt=fmt, filename=names.get(e)))
    return out_paths
