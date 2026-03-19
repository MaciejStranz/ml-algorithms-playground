from __future__ import annotations

from typing import Any, Dict, List

from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

from ml_core.common.types import ParamType
from ml_core.common.hyperparameters import HyperparameterSpec


def rf_classifier_factory(params: Dict[str, Any]):
    return RandomForestClassifier(**(params or {}))


def rf_regressor_factory(params: Dict[str, Any]):
    return RandomForestRegressor(**(params or {}))


def rf_base_specs() -> List[HyperparameterSpec]:
    """
    Specs shared by RF classifier and regressor.
    No applicable_tasks here - variants define compatibility.
    """
    return [
        HyperparameterSpec(
            name="n_estimators",
            display_name="Number of trees",
            type=ParamType.INT,
            default=100,
            min=10,
            max=2000,
            description="The number of trees in the forest.",
        ),
        HyperparameterSpec(
            name="max_depth",
            display_name="Max tree depth",
            type=ParamType.INT,
            default=None,
            nullable = True,
            min=1,
            max=50,
            description=(
                "The maximum depth of each tree. If None, nodes are expanded until all "
                "leaves are pure or contain fewer samples than min_samples_split."
            ),
        ),
        HyperparameterSpec(
            name="min_samples_split",
            display_name="Min samples split",
            type=ParamType.INT,
            default=2,
            min=2,
            max=100,
            description="The minimum number of samples required to split an internal node.",
        ),
        HyperparameterSpec(
            name="min_samples_leaf",
            display_name="Min samples leaf",
            type=ParamType.INT,
            default=1,
            min=1,
            max=100,
            description="The minimum number of samples required to be at a leaf node.",
        ),
        HyperparameterSpec(
            name="max_features",
            display_name="Max features",
            type=ParamType.NUMBER_OR_STRING,
            default=1.0,
            choices=["sqrt", "log2"],
            description=(
                "The number of features to consider when looking for the best split. "
                "Can be an integer, float (fraction), or one of: 'sqrt', 'log2'."
            ),
        ),
    ]

def rf_classification_specs() -> List[HyperparameterSpec]:
    return [
        HyperparameterSpec(
            name="criterion",
            display_name="Criterion",
            type=ParamType.CHOICE,
            default="gini",
            choices=["gini", "entropy", "log_loss"],
            description="The function to measure the quality of a split.",
        ),
    ]

def rf_regression_specs() -> List[HyperparameterSpec]:
    return [
        HyperparameterSpec(
            name="criterion",
            display_name="Criterion",
            type=ParamType.CHOICE,
            default="squared_error",
            choices=["squared_error", "absolute_error", "friedman_mse", "poisson"],
            description="The function to measure the quality of a split.",
        ),
    ]


