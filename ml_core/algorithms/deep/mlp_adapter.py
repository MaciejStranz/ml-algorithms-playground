from __future__ import annotations

from typing import Any, Dict, List

from ml_core.common.types import ParamType
from ml_core.common.hyperparameters import HyperparameterSpec
from ml_core.algorithms.deep.mlp import MLPClassifier, MLPRegressor


def mlp_classifier_factory(params: Dict[str, Any]) -> Any:
    params = dict(params or {})
    params.setdefault("hidden_dims", [64, 64])
    return MLPClassifier(**params)


def mlp_regressor_factory(params: Dict[str, Any]) -> Any:
    params = dict(params or {})
    params.setdefault("hidden_dims", [64, 64])
    return MLPRegressor(**params)


def mlp_specs() -> List[HyperparameterSpec]:
    return [
        HyperparameterSpec(
            name="hidden_dims",
            display_name="Hidden layer sizes",
            type=ParamType.INT_LIST,
            default=[64, 64],
            description="List of hidden layer sizes, e.g. [64, 64] or [128, 64, 32].",
        ),
        HyperparameterSpec(
            name="activation",
            display_name="Activation function",
            type=ParamType.CHOICE,
            default="relu",
            choices=["relu", "tanh", "gelu"],
            description="Non-linear activation used between layers.",
        ),
        HyperparameterSpec(
            name="dropout",
            display_name="Dropout",
            type=ParamType.FLOAT,
            default=0.0,
            min=0.0,
            max=0.8,
            description="Dropout probability applied after each hidden layer.",
        ),
        HyperparameterSpec(
            name="lr",
            display_name="Learning rate",
            type=ParamType.FLOAT,
            default=1e-3,
            min=1e-6,
            max=1e-1,
            description="Learning rate for the Adam optimizer.",
        ),
        HyperparameterSpec(
            name="batch_size",
            display_name="Batch size",
            type=ParamType.INT,
            default=64,
            min=1,
            max=4096,
            description="Mini-batch size used during training.",
        ),
        HyperparameterSpec(
            name="max_epochs",
            display_name="Max epochs",
            type=ParamType.INT,
            default=100,
            min=1,
            max=10000,
            description="Maximum number of training epochs.",
        ),
        HyperparameterSpec(
            name="weight_decay",
            display_name="Weight decay (L2 regularization)",
            type=ParamType.FLOAT,
            default=0.0,
            min=0.0,
            max=1.0,
            description="L2 weight decay used by the Adam optimizer.",
        ),
    ]
