from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ml_core.common.types import TaskFamily
from ml_core.common.hyperparameters import HyperparameterSpec


ModelFactory = Callable[[Dict[str, Any]], Any]


@dataclass(frozen=True)
class AlgorithmVariant:
    """
    A concrete implementation of an algorithm for a given TaskFamily.
    Example: SVM classifier vs SVM regressor.
    """
    family: TaskFamily
    factory: ModelFactory
    hyperparams: List[HyperparameterSpec]


@dataclass(frozen=True)
class AlgorithmDefinition:
    """
    Algorithm definition that may have multiple variants.
    Example: SVM -> {classification, regression}.
    """
    code: str
    name: str
    kind: str  # "classical" | "deep"
    description: str
    variants: Dict[TaskFamily, AlgorithmVariant]

    def get_variant(self, family: TaskFamily) -> AlgorithmVariant:
        try:
            return self.variants[family]
        except KeyError:
            available = ", ".join(v.value for v in self.variants.keys())
            raise ValueError(
                f"Algorithm {self.code!r} does not support {family.value!r}. "
                f"Available families: {available}"
            ) from None
