from __future__ import annotations

from typing import Any, Dict, List

from sklearn.linear_model import LinearRegression, LogisticRegression

from ml_core.common.types import ParamType
from ml_core.common.hyperparameters import HyperparameterSpec


def regression_classifier_factory(params: Dict[str, Any]):
    """
    LogisticRegression for classification tasks.
    """
    params = params or {}
    return LogisticRegression(**{"max_iter": 1000, "solver": "saga", **params})


def regression_regressor_factory(params: Dict[str, Any]):
    """
    LinearRegression for regression tasks.
    """
    return LinearRegression(**(params or {}))


def regression_classification_specs() -> List[HyperparameterSpec]:
    """
    Hyperparameters exposed for LogisticRegression.

    No applicable_tasks here — variant is classification by design.
    """
    return [
        HyperparameterSpec(
            name="C",
            display_name="C (Inverse regularization strength)",
            type=ParamType.FLOAT,
            default=1.0,
            min=1e-4,
            max=1e4,
            description=(
                "Inverse of regularization strength for LogisticRegression. "
                "Smaller values specify stronger regularization."
            ),
        ),
        HyperparameterSpec(
            name="l1_ratio",
            display_name="l1 ratio",
            type=ParamType.FLOAT,
            default=0.0,
            description=(
                "The Elastic-Net mixing parameter, with 0 <= l1_ratio <= 1. Setting l1_ratio=1 gives a pure L1-penalty, "
                "setting l1_ratio=0 a pure L2-penalty. Any value between 0 and 1 gives an Elastic-Net penalty of the"
                " form l1_ratio * L1 + (1 - l1_ratio) * L2"
            ),
        ),
        HyperparameterSpec(
            name="fit_intercept",
            display_name="Fit intercept",
            type=ParamType.BOOL,
            default=True,
            description="Specifies if a constant (a.k.a. bias or intercept) should be added to the decision function.",
        ),
    ]


def regression_regression_specs() -> List[HyperparameterSpec]:
    """
    Hyperparameters exposed for LinearRegression.

    Note: LinearRegression does not have 'C'/'penalty'. We expose only a small,
    stable subset to keep the UI and validation consistent.
    """
    return [
        HyperparameterSpec(
            name="fit_intercept",
            display_name="Fit intercept",
            type=ParamType.BOOL,
            default=True,
            description="Whether to calculate the intercept for this model. " \
            "If set to False, no intercept will be used in calculations (i.e. data is expected to be centered).",
        ),
    ]
