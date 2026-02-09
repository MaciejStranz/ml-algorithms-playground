from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional

from ml_core.common.types import TaskType
from ml_core.common.hyperparameters import HyperparameterSpec


ModelFactory = Callable[[Dict[str, Any]], Any]


@dataclass(frozen=True)
class AlgorithmVariant:
    """
    Concrete implementation of an algorithm that supports one or more TaskTypes.
    Example:
      - SVC supports [binary classification, multiclass classification]
      - SVR supports [regression]
    """
    code: str 
    supported_tasks: List[TaskType]
    factory: ModelFactory
    hyperparams: List[HyperparameterSpec]

    def supports(self, task: TaskType) -> bool:
        return task in self.supported_tasks


@dataclass(frozen=True)
class AlgorithmDefinition:
    """
    Algorithm definition that may have multiple variants.
    Example: SVM -> {classification(same for binary and multiclass), regression}.
    """
    code: str
    name: str
    kind: str  # "classical" | "deep"
    description: str
    variants: List[AlgorithmVariant]

    def get_variant(self, task: TaskType) -> AlgorithmVariant:
        for variant in self.variants:
            if variant.supports(task):
                return variant
        available = ", ".join(
            sorted({task.value for variant in self.variants for task in variant.supported_tasks})
        )
        raise ValueError(
            f"Algorithm {self.code!r} does not support task {task.value!r}. "
            f"Supported tasks: {available}"
        )

