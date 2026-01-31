from __future__ import annotations

from ml_core.algorithms.algorithm_registry import AlgorithmDefinition, AlgorithmVariant
from ml_core.common.types import TaskFamily

from ml_core.algorithms.deep.mlp_adapter import (
    mlp_classifier_factory,
    mlp_regressor_factory,
    mlp_specs,
)

MLP_DEFINITION = AlgorithmDefinition(
    code="mlp",
    name="Neural Network (MLP, PyTorch)",
    kind="deep",
    description="Torch-based MLP with sklearn-like API.",
    variants={
        TaskFamily.CLASSIFICATION: AlgorithmVariant(
            family=TaskFamily.CLASSIFICATION,
            factory=mlp_classifier_factory,
            hyperparams=mlp_specs(),
        ),
        TaskFamily.REGRESSION: AlgorithmVariant(
            family=TaskFamily.REGRESSION,
            factory=mlp_regressor_factory,
            hyperparams=mlp_specs(),
        ),
    },
)
