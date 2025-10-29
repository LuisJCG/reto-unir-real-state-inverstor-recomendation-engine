from abc import ABC, abstractmethod
from typing import Dict, Any, List

class EntityGenerator(ABC):
    @abstractmethod
    def generate(self, n: int) -> List[Dict[str, Any]]:
        ...

class GeneratorFactory:
    _registry = {}

    @classmethod
    def register(cls, name: str, gen_cls):
        cls._registry[name] = gen_cls

    @classmethod
    def create(cls, name: str, **kwargs) -> EntityGenerator:
        if name not in cls._registry:
            raise ValueError(f"Unknown generator '{name}'. Registered: {list(cls._registry.keys())}")
        return cls._registry[name](**kwargs)
