from __future__ import annotations

from ml_core.algorithms.algorithm_registry import AlgorithmDefinition, AlgorithmVariant
from ml_core.common.types import TaskFamily #do usuniecia
from ml_core.common.types import TaskType

from ml_core.algorithms.classical_algorithms.svm import (
    svm_classifier_factory,
    svm_regressor_factory,
    svm_base_specs,
    svm_regression_specs,
)
from ml_core.algorithms.classical_algorithms.random_forest import (
    rf_classifier_factory,
    rf_regressor_factory,
    rf_base_specs,
    rf_classification_specs,
    rf_regression_specs
)
from ml_core.algorithms.classical_algorithms.xgboost import (
    xgb_classifier_factory,
    xgb_regressor_factory,
    xgb_base_specs,
)
from ml_core.algorithms.classical_algorithms.regression import (
    regression_classifier_factory,
    regression_regressor_factory,
    regression_classification_specs,
    regression_regression_specs,
)


SVM_DEFINITION = AlgorithmDefinition(
    code="svm",
    name="Support Vector Machine",
    kind="classical",
    description="Support Vector Machine classifier/regressor with various kernels.",
    variants=[
        AlgorithmVariant(
            code="svc",
            supported_tasks=[TaskType.BINARY, TaskType.MULTICLASS],
            factory=svm_classifier_factory,
            hyperparams=svm_base_specs()
        ),
        AlgorithmVariant(
            code="svr",
            supported_tasks=[TaskType.REGRESSION],
            factory=svm_regressor_factory,
            hyperparams=svm_base_specs() + svm_regression_specs()
        ),
    ]
)

RF_DEFINITION = AlgorithmDefinition(
    code="random_forest",
    name="Random Forest",
    kind="classical",
    description="Ensemble of decision trees for classification and regression.",
    variants=[
        AlgorithmVariant(
            code="rf_classifier",
            supported_tasks=[TaskType.BINARY, TaskType.MULTICLASS],
            factory=rf_classifier_factory,
            hyperparams=rf_base_specs() + rf_classification_specs(),
        ),
        AlgorithmVariant(
            code="rf_regressor",
            supported_tasks=[TaskType.REGRESSION],
            factory=rf_regressor_factory,
            hyperparams=rf_base_specs() + rf_regression_specs(),
        ),
    ],
)


XGB_DEFINITION = AlgorithmDefinition(
    code="xgboost",
    name="XGBoost",
    kind="classical",
    description="Gradient boosting trees (XGBoost) for structured data.",
    variants=[
        AlgorithmVariant(
            code="xgb_classifier",
            supported_tasks=[TaskType.BINARY, TaskType.MULTICLASS],
            factory=xgb_classifier_factory,
            hyperparams=xgb_base_specs(),
        ),
        AlgorithmVariant(
            code="xgb_regressor",
            supported_tasks=[TaskType.REGRESSION],
            factory=xgb_regressor_factory,
            hyperparams=xgb_base_specs(),
        ),
    ],
)


REGRESSION_DEFINITION = AlgorithmDefinition(
    code="regression",
    name="Logistic / Linear Regression",
    kind="classical",
    description="LogisticRegression for classification, LinearRegression for regression.",
    variants=[
        AlgorithmVariant(
            code="log_reg",
            supported_tasks=[TaskType.BINARY, TaskType.MULTICLASS],
            factory=regression_classifier_factory,
            hyperparams=regression_classification_specs(),
        ),
        AlgorithmVariant(
            code="lin_reg",
            supported_tasks=[TaskType.REGRESSION],
            factory=regression_regressor_factory,
            hyperparams=regression_regression_specs(),
        ),
    ],
)


