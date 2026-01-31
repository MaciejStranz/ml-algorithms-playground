from __future__ import annotations

from typing import Any, Dict, List

from xgboost import XGBClassifier, XGBRegressor

from ml_core.common.types import ParamType
from ml_core.common.hyperparameters import HyperparameterSpec


def xgb_classifier_factory(params: Dict[str, Any]):
    """
    XGBClassifier for classification tasks.
    """
    return XGBClassifier(**(params or {}))


def xgb_regressor_factory(params: Dict[str, Any]):
    """
    XGBRegressor for regression tasks.
    """
    return XGBRegressor(**(params or {}))


def xgb_base_specs() -> List[HyperparameterSpec]:
    """
    Specs shared by XGBoost classifier and regressor.

    IMPORTANT:
    - No applicable_tasks here.
    - Variant selection (TaskFamily) decides compatibility.
    """
    return [
        HyperparameterSpec(
            name="n_estimators",
            display_name="Number of trees",
            type=ParamType.INT,
            default=100,
            min=10,
            max=3000,
            description="Number of boosting stages (trees) to fit.",
        ),
        HyperparameterSpec(
            name="learning_rate",
            display_name="Learning rate",
            type=ParamType.FLOAT,
            default=0.3,
            min=1e-4,
            max=1.0,
            description=(
                "Shrinkage factor applied to each tree's contribution. "
                "Smaller values require more trees but can lead to better generalization."
            ),
        ),
        HyperparameterSpec(
            name="max_depth",
            display_name="Max tree depth",
            type=ParamType.INT,
            default=6,
            min=1,
            max=20,
            description="Maximum depth of individual trees.",
        ),
        HyperparameterSpec(
            name="subsample",
            display_name="Subsample",
            type=ParamType.FLOAT,
            default=1.0,
            min=0.1,
            max=1.0,
            description=(
                "Subsample ratio of the training instances. Values < 1.0 act as row-wise "
                "subsampling and can reduce overfitting."
            ),
        ),
        HyperparameterSpec(
            name="colsample_bytree",
            display_name="Column subsample (by tree)",
            type=ParamType.FLOAT,
            default=1.0,
            min=0.1,
            max=1.0,
            description=(
                "Subsample ratio of columns when constructing each tree. Acts as feature "
                "subsampling and can reduce overfitting."
            ),
        ),
        HyperparameterSpec(
            name="reg_lambda",
            display_name="L2 regularization (lambda)",
            type=ParamType.FLOAT,
            default=1.0,
            min=0.0,
            max=100.0,
            description="L2 regularization term on weights.",
        ),
        HyperparameterSpec(
            name="reg_alpha",
            display_name="L1 regularization (alpha)",
            type=ParamType.FLOAT,
            default=0.0,
            min=0.0,
            max=100.0,
            description="L1 regularization term on weights.",
        ),
    ]

