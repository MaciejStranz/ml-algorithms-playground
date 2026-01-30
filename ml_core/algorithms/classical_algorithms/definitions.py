from __future__ import annotations

from ml_core.algorithms.algorithm_registry import AlgorithmDefinition, AlgorithmVariant
from ml_core.common.types import TaskFamily

from ml_core.algorithms.classical_algorithms.svm import (
    svm_classifier_factory,
    svm_regressor_factory,
    svm_base_specs,
    svm_regression_only_specs,
)


SVM_DEFINITION = AlgorithmDefinition(
    code="svm",
    name="Support Vector Machine",
    kind="classical",
    description="Support Vector Machine classifier/regressor with various kernels.",
    variants={
        TaskFamily.CLASSIFICATION: AlgorithmVariant(
            family=TaskFamily.CLASSIFICATION,
            factory=svm_classifier_factory,
            hyperparams=svm_base_specs(),
        ),
        TaskFamily.REGRESSION: AlgorithmVariant(
            family=TaskFamily.REGRESSION,
            factory=svm_regressor_factory,
            hyperparams=svm_base_specs() + svm_regression_only_specs(),
        ),
    },
)
