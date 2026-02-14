from __future__ import annotations

from typing import Any, Dict, List

from ml_core.algorithms.algorithm_registry import AlgorithmDefinition
from ml_core.algorithms.classical_algorithms.definitions import (SVM_DEFINITION, RF_DEFINITION, 
                                                                 XGB_DEFINITION, REGRESSION_DEFINITION)
from ml_core.algorithms.deep.definitions import MLP_DEFINITION


ALGORITHMS: Dict[str, AlgorithmDefinition] = {
    SVM_DEFINITION.code: SVM_DEFINITION,
    RF_DEFINITION.code: RF_DEFINITION,
    XGB_DEFINITION.code: XGB_DEFINITION,
    REGRESSION_DEFINITION.code: REGRESSION_DEFINITION,
    MLP_DEFINITION.code: MLP_DEFINITION,
}


def get_algorithm(code: str) -> AlgorithmDefinition:
    try:
        return ALGORITHMS[code]
    except KeyError:
        available = ", ".join(sorted(ALGORITHMS.keys()))
        raise ValueError(f"Unknown algorithm {code!r}. Available: {available}") from None


def export_algorithms_for_backend() -> List[Dict[str, Any]]:
    """
    Return algorithms/variants metadata as plain JSON-friendly structures.

    Shape:
    [
      {
        "code": "svm",
        "name": "Support Vector Machine",
        "kind": "classical",
        "description": "...",
        "variants": [
          {
            "code": "svc",
            "supported_tasks": ["binary_classification", "multiclass_classification"],
            "hyperparameter_specs": [ { ... }, ... ]
          },
          ...
        ]
      },
      ...
    ]
    """
    exported: List[Dict[str, Any]] = []

    for algo_code, definition in ALGORITHMS.items():
        algo_dict: Dict[str, Any] = {
            "code": str(definition.code or algo_code),
            "name": str(definition.name),
            "kind": str(definition.kind),
            "description": str(definition.description or ""),
            "variants": [],
        }

        for v in definition.variants:
            variant_dict: Dict[str, Any] = {
                "code": str(v.code),
                "supported_tasks": [t.value for t in (v.supported_tasks or [])],
                "hyperparameter_specs": [s.to_dict() for s in (v.hyperparams or [])],
            }
            algo_dict["variants"].append(variant_dict)

        exported.append(algo_dict)

    return exported