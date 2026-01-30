from __future__ import annotations

from typing import Any, Dict, List

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC, SVR

from ml_core.common.types import ParamType
from ml_core.common.hyperparameters import HyperparameterSpec


def svm_classifier_factory(params: Dict[str, Any] | None):
    params = params or {}
    # SVC supports predict_proba only if probability=True
    base = SVC(**{"probability": True, **(params)})
    return make_pipeline(StandardScaler(), base)


def svm_regressor_factory(params: Dict[str, Any] | None):
    params = params or {}
    base = SVR(**(params))
    return make_pipeline(StandardScaler(), base)


def svm_base_specs() -> List[HyperparameterSpec]:
    return [
        HyperparameterSpec(
            name="C",
            display_name="C (Regularization strength)",
            type=ParamType.FLOAT,
            default=1.0,
            min=1e-4,
            max=1e4,
            description=(
                "Inverse of regularization strength for SVM. "
                "Smaller values specify stronger regularization."
            ),
        ),
        HyperparameterSpec(
            name="kernel",
            display_name="Kernel",
            type=ParamType.CHOICE,
            default="rbf",
            choices=["linear", "rbf", "poly", "sigmoid"],
            description="Kernel type used by SVM.",
        ),
        HyperparameterSpec(
            name="gamma",
            display_name="Gamma",
            type=ParamType.NUMBER_OR_STRING,
            default="scale",
            min=1e-6,
            max=1e3,
            choices=["scale", "auto"],
            description="Kernel coefficient for rbf/poly/sigmoid.",
        ),
    ]


def svm_regression_only_specs() -> List[HyperparameterSpec]:
    return [
        HyperparameterSpec(
            name="epsilon",
            display_name="Epsilon (SVR only)",
            type=ParamType.FLOAT,
            default=0.1,
            min=0.0,
            max=10.0,
            description="Epsilon-tube width used in SVR loss.",
        ),
    ]
