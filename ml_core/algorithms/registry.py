# ml_core/algorithms/registry.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List

from ml_core.common.types import TaskType
from ml_core.algorithms.hparam_specs import get_hyperparameter_specs_as_dicts


@dataclass
class AlgorithmMeta:
    code: str                    # "svm"
    name: str                    # "Support Vector Machine"
    kind: str                    # "classical" | "deep"
    description: str = ""


ALGORITHMS: List[AlgorithmMeta] = [
    AlgorithmMeta(
        code="svm",
        name="Support Vector Machine",
        kind="classical",
        description="Support Vector Machine classifier/regressor with various kernels.",
    ),
    AlgorithmMeta(
        code="random_forest",
        name="Random Forest",
        kind="classical",
        description="Ensemble of decision trees for classification and regression.",
    ),
    AlgorithmMeta(
        code="xgboost",
        name="XGBoost",
        kind="classical",
        description="Gradient boosting trees (XGBoost) for structured data.",
    ),
    AlgorithmMeta(
        code="regression",
        name="Logistic / Linear Regression",
        kind="classical",
        description="LogisticRegression for classification, LinearRegression for regression.",
    ),
    AlgorithmMeta(
        code="mlp",
        name="Neural Network (MLP, PyTorch)",
        kind="deep",
        description="Fully-connected neural network implemented in PyTorch.",
    ),
]


def get_all_algorithms_meta() -> List[Dict[str, Any]]:
    """
    Returns a list of dictionaries ready for JSON serialization or storage in Django.
    Combines algorithm metadata with its hyperparameter specifications.
    """
    result: List[Dict[str, Any]] = []
    for alg in ALGORITHMS:
        hparam_specs = get_hyperparameter_specs_as_dicts(alg.code, task=None)

        result.append(
            {
                "code": alg.code,
                "name": alg.name,
                "kind": alg.kind,
                "description": alg.description,
                "hyperparameter_specs": hparam_specs,
            }
        )
    return result
