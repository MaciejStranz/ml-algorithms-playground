# ml_core/algorithms/hparam_specs.py

from __future__ import annotations

from typing import Any, Dict, List

from ml_core.common.types import TaskType, ParamType
from ml_core.common.hyperparameters import (
    HyperparameterSpec,
    specs_to_dict_list,
    validate_params_against_specs,
)

#  SVM Hyperparameters

SVM_HPARAMS: List[HyperparameterSpec] = [
    HyperparameterSpec(
        name="C",
        display_name="C (Regularization strength)",
        type=ParamType.FLOAT,
        default=1.0,
        min=1e-4,
        max=1e4,
        description=(
            "Inverse of regularization strength for SVM. "
            "Smaller values specify stronger regularization. "
            "Larger values allow more complex decision boundaries."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="kernel",
        display_name="Kernel",
        type=ParamType.CHOICE,
        default="rbf",
        choices=["linear", "rbf", "poly", "sigmoid"],
        description=(
            "Specifies the kernel type to be used in the algorithm. "
            "'linear' works well for approximately linear problems; "
            "'rbf' and 'poly' capture nonlinear relationships."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="gamma",
        display_name="Gamma",
        type=ParamType.NUMBER_OR_STRING,
        default="scale",
        min=1e-6,
        max=1e3,
        choices=["scale", "auto"],  # allowed string values
        description=(
            "Kernel coefficient for 'rbf', 'poly' and 'sigmoid'. "
            "Can be a float value or one of 'scale'/'auto'. "
            "For 'linear' kernel this parameter is ignored by sklearn."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="epsilon",
        display_name="Epsilon (SVR only)",
        type=ParamType.FLOAT,
        default=0.1,
        min=0.0,
        max=10.0,
        description=(
            "Epsilon in the epsilon-SVR model. It specifies the epsilon-tube "
            "within which no penalty is associated in the training loss. "
            "Only used for regression tasks (SVR)."
        ),
        applicable_tasks=[TaskType.REGRESSION],
        advanced=True,
    ),
]


#  Random Forest Hyperparameters


RF_HPARAMS: List[HyperparameterSpec] = [
    HyperparameterSpec(
        name="n_estimators",
        display_name="Number of trees",
        type=ParamType.INT,
        default=100,
        min=10,
        max=2000,
        description="The number of trees in the forest.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="max_depth",
        display_name="Max tree depth",
        type=ParamType.INT,
        default=None,
        min=1,
        max=50,
        description=(
            "The maximum depth of each tree. "
            "If None, nodes are expanded until all leaves are pure or contain "
            "fewer samples than min_samples_split."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="min_samples_split",
        display_name="Min samples split",
        type=ParamType.INT,
        default=2,
        min=2,
        max=100,
        description=(
            "The minimum number of samples required to split an internal node."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="min_samples_leaf",
        display_name="Min samples leaf",
        type=ParamType.INT,
        default=1,
        min=1,
        max=100,
        description=(
            "The minimum number of samples required to be at a leaf node."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="max_features",
        display_name="Max features",
        type=ParamType.NUMBER_OR_STRING,
        default="auto",
        # For RandomForest, max_features can be:
        # - int (number of features),
        # - float (fraction of features),
        # - string: 'auto', 'sqrt', 'log2'
        choices=["auto", "sqrt", "log2"],
        description=(
            "The number of features to consider when looking for the best split. "
            "Can be an integer (number of features), a float (fraction of features), "
            "or one of 'auto', 'sqrt', 'log2'. Validation here only checks that the "
            "value is either numeric or one of the supported strings; detailed "
            "semantics are handled by sklearn."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
]


#  XGBoost Hyperparameters


XGB_HPARAMS: List[HyperparameterSpec] = [
    HyperparameterSpec(
        name="n_estimators",
        display_name="Number of trees",
        type=ParamType.INT,
        default=100,
        min=10,
        max=3000,
        description="Number of boosting stages (trees) to fit.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
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
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="max_depth",
        display_name="Max tree depth",
        type=ParamType.INT,
        default=6,
        min=1,
        max=20,
        description="Maximum depth of individual trees.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="subsample",
        display_name="Subsample",
        type=ParamType.FLOAT,
        default=1.0,
        min=0.1,
        max=1.0,
        description=(
            "Subsample ratio of the training instances. "
            "Values < 1.0 act as row-wise subsampling and can reduce overfitting."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="colsample_bytree",
        display_name="Column subsample (by tree)",
        type=ParamType.FLOAT,
        default=1.0,
        min=0.1,
        max=1.0,
        description=(
            "Subsample ratio of columns when constructing each tree. "
            "Acts as feature subsampling and can reduce overfitting."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="reg_lambda",
        display_name="L2 regularization (lambda)",
        type=ParamType.FLOAT,
        default=1.0,
        min=0.0,
        max=100.0,
        description="L2 regularization term on weights.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="reg_alpha",
        display_name="L1 regularization (alpha)",
        type=ParamType.FLOAT,
        default=0.0,
        min=0.0,
        max=100.0,
        description="L1 regularization term on weights.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
]


#  Logistic / Linear Regression Hyperparameters


REGRESSION_HPARAMS: List[HyperparameterSpec] = [
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
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS],
    ),
    HyperparameterSpec(
        name="penalty",
        display_name="Penalty",
        type=ParamType.CHOICE,
        default="l2",
        choices=["l2", "none"],
        description=(
            "Norm used in the penalization for LogisticRegression. "
            "Not all penalties are supported by all solvers. "
            "For simplicity, only 'l2' and 'none' are exposed here."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS],
        advanced=True,
    ),
    HyperparameterSpec(
        name="fit_intercept",
        display_name="Fit intercept",
        type=ParamType.BOOL,
        default=True,
        description="Whether to calculate the intercept for the model.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
]

#  MLP (Torch) Hyperparameters

MLP_HPARAMS: List[HyperparameterSpec] = [
    HyperparameterSpec(
        name="hidden_dims",
        display_name="Hidden layer sizes",
        type=ParamType.INT_LIST,
        default=[64, 64],
        description=(
            "List of hidden layer sizes, e.g. [64, 64] or [128, 64, 32]. "
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="activation",
        display_name="Activation function",
        type=ParamType.CHOICE,
        default="relu",
        choices=["relu", "tanh", "gelu"],
        description="Non-linear activation used between layers.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="dropout",
        display_name="Dropout",
        type=ParamType.FLOAT,
        default=0.0,
        min=0.0,
        max=0.8,
        description=(
            "Dropout probability applied after each hidden layer. "
            "Use values in [0.0, 0.5] for regularization. 0.0 disables dropout."
        ),
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
    HyperparameterSpec(
        name="lr",
        display_name="Learning rate",
        type=ParamType.FLOAT,
        default=1e-3,
        min=1e-6,
        max=1e-1,
        description="Learning rate for the Adam optimizer.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="batch_size",
        display_name="Batch size",
        type=ParamType.INT,
        default=64,
        min=1,
        max=4096,
        description="Mini-batch size used during training.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="max_epochs",
        display_name="Max epochs",
        type=ParamType.INT,
        default=100,
        min=1,
        max=10000,
        description="Maximum number of training epochs.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
    ),
    HyperparameterSpec(
        name="weight_decay",
        display_name="Weight decay (L2 regularization)",
        type=ParamType.FLOAT,
        default=0.0,
        min=0.0,
        max=1.0,
        description="L2 weight decay used by the Adam optimizer.",
        applicable_tasks=[TaskType.BINARY, TaskType.MULTICLASS, TaskType.REGRESSION],
        advanced=True,
    ),
]


#  Registry and helpers

ALGORITHM_HPARAMS: Dict[str, List[HyperparameterSpec]] = {
    "svm": SVM_HPARAMS,
    "random_forest": RF_HPARAMS,
    "xgboost": XGB_HPARAMS,
    "regression": REGRESSION_HPARAMS,
    "mlp" : MLP_HPARAMS,
}


def get_hyperparameter_specs(
    algorithm_name: str,
    task: TaskType | None = None,
) -> List[HyperparameterSpec]:
    """
    Return the list of HyperparameterSpec objects for a given algorithm,
    optionally filtered by task type.
    """
    try:
        specs = ALGORITHM_HPARAMS[algorithm_name]
    except KeyError:
        available = ", ".join(sorted(ALGORITHM_HPARAMS.keys()))
        raise ValueError(
            f"Unknown algorithm {algorithm_name!r}. Available: {available}"
        ) from None

    if task is None:
        return list(specs)

    return [
        s for s in specs
        if s.applicable_tasks is None or task in s.applicable_tasks
    ]


def get_hyperparameter_specs_as_dicts(
    algorithm_name: str,
    task: TaskType | None = None,
) -> List[Dict[str, Any]]:
    """
    Convenience helper for exposing specs to the outside world (e.g. backend/frontend).
    """
    specs = get_hyperparameter_specs(algorithm_name, task)
    return specs_to_dict_list(specs)


def validate_hyperparameters(
    algorithm_name: str,
    task: TaskType,
    user_params: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate user-provided hyperparameters for a given algorithm and task.

    - Unknown parameters are rejected.
    - Values are validated w.r.t. type, range, and choices.
    - Cross-parameter semantics (e.g. exact interactions between parameters)
      are intentionally left to the underlying ML library (sklearn, xgboost),
      to avoid duplicating their logic.

    Returns a sanitized dict that can be safely forwarded to the model factory.
    """
    specs_list = get_hyperparameter_specs(algorithm_name, task)
    specs_map = {s.name: s for s in specs_list}
    return validate_params_against_specs(specs_map, user_params)
