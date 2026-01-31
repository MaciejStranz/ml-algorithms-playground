from __future__ import annotations

from typing import Dict

from ml_core.algorithms.algorithm_registry import AlgorithmDefinition
from ml_core.algorithms.classical_algorithms.definitions import SVM_DEFINITION, RF_DEFINITION, XGB_DEFINITION


ALGORITHMS: Dict[str, AlgorithmDefinition] = {
    SVM_DEFINITION.code: SVM_DEFINITION,
    RF_DEFINITION.code: RF_DEFINITION,
    XGB_DEFINITION.code: XGB_DEFINITION,
    # later: xgboost, regression, mlp...
}


def get_algorithm(code: str) -> AlgorithmDefinition:
    try:
        return ALGORITHMS[code]
    except KeyError:
        available = ", ".join(sorted(ALGORITHMS.keys()))
        raise ValueError(f"Unknown algorithm {code!r}. Available: {available}") from None
