# ml_core/runner.py

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import numpy as np

from ml_core.data_handlers.load_dataset import load_data, Dataset
from ml_core.data_handlers.metadata import DatasetMeta, TaskType
from ml_core.algorithms.classical import get_classical_model
from ml_core.algorithms.deep.mlp import get_deep_model
from ml_core.evaluation.metrics import EvaluationReport
from ml_core.algorithms.hparam_specs import validate_hyperparameters

#  Public config model
@dataclass
class RunConfig:
    """
    High-level configuration for a single training + evaluation run.

    This is the structure the backend should map its request body onto.
    """

    dataset_name: str               # e.g. "iris", "wine", "breast_cancer", "diabetes", "sinx"
    algorithm_name: str             # e.g. "svm", "random_forest", "xgboost", "logistic", "mlp"
    hyperparams: Dict[str, Any] | None = None

    # Dataset split config
    test_size: float = 0.3
    random_state: int = 42

    # Output config
    include_predictions: bool = True
    include_probabilities: bool = False  # only used for classification tasks

#  Internal helpers

_DEEP_ALGORITHMS = {"mlp"}


def _build_model(
    algorithm_name: str,
    task: TaskType,
    hyperparams: Dict[str, Any] | None,
):
    """
    Construct a model instance based on algorithm name and task.

    - All algorithms (including MLP) przechodzą przez walidację hiperparametrów
      w oparciu o HyperparameterSpec (validate_hyperparameters).
    - Modele klasyczne używają get_classical_model.
    - Modele głębokie używają get_deep_model.
    """
    hyperparams = hyperparams or {}

    validated_params = validate_hyperparameters(
        algorithm_name=algorithm_name,
        task=task,
        user_params=hyperparams,
    )

    if algorithm_name in _DEEP_ALGORITHMS:
        return get_deep_model(
            name=algorithm_name,
            task=task,
            params=validated_params,
        )

    return get_classical_model(
        name=algorithm_name,
        task=task,
        params=validated_params,
    )


def _predictions_to_dict(
    dataset: Dataset,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None,
) -> Dict[str, Any]:
    """
    Serialize predictions and ground truth for potential plotting / inspection.
    """
    y_true = dataset.y_test

    result: Dict[str, Any] = {
        "y_true": y_true.tolist(),
        "y_pred": y_pred.tolist(),
    }

    if y_proba is not None:
        result["y_proba"] = y_proba.tolist()

    if dataset.meta.task in (TaskType.BINARY, TaskType.MULTICLASS):
        result["class_labels"] = (
            list(dataset.meta.class_labels) if dataset.meta.class_labels is not None else None
        )

    return result


def _predict_proba(
    model: Any,
    X: np.ndarray,
    task: TaskType,
    include_probabilities: bool,
) -> Optional[np.ndarray]:
    """
    Optionally compute predict_proba for classification tasks, if the model supports it.
    """
    if not include_probabilities:
        return None

    if task not in (TaskType.BINARY, TaskType.MULTICLASS):
        return None

    # Some models may not implement predict_proba (e.g. certain custom models).
    if not hasattr(model, "predict_proba"):
        return None

    proba = model.predict_proba(X)
    proba = np.asarray(proba)
    return proba


#  Public entrypoint


def run_experiment(config: RunConfig) -> Dict[str, Any]:
    """
    High-level training + evaluation entrypoint.

    This is the main function that the backend should call.

    Steps:
    1. Load dataset and split into train/test.
    2. Build model (classical or deep) with hyperparameter validation.
    3. Fit model on train.
    4. Predict on test (optionally predict_proba).
    5. Compute metrics via EvaluationReport.
    6. Return everything as a JSON-serializable dict.
    """
    # 1. Load dataset
    dataset = load_data(
        name=config.dataset_name,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    # 2. Build model
    model = _build_model(
        algorithm_name=config.algorithm_name,
        task=dataset.meta.task,
        hyperparams=config.hyperparams,
    )

    # 3. Fit
    model.fit(dataset.X_train, dataset.y_train)

    # 4. Predict
    y_pred = model.predict(dataset.X_test)
    y_pred = np.asarray(y_pred)

    # 4b. Optionally predict probabilities for classification
    y_proba = _predict_proba(
        model=model,
        X=dataset.X_test,
        task=dataset.meta.task,
        include_probabilities=config.include_probabilities,
    )

    # 5. Evaluation
    report = EvaluationReport(
        y_true=dataset.y_test,
        y_pred=y_pred,
        task=dataset.meta.task,
        target_names=dataset.meta.class_labels,
    )

    # 6. Assemble result
    result: Dict[str, Any] = {
        "dataset": dataset.meta.to_dict(),
        "algorithm": {
            "name": config.algorithm_name,
            "kind": "deep" if config.algorithm_name in _DEEP_ALGORITHMS else "classical",
            "hyperparams": config.hyperparams or {},
        },
        "metrics": report.summary() # _evaluation_to_dict(report),
    }

    if config.include_predictions:
        result["predictions"] = _predictions_to_dict(dataset, y_pred, y_proba)

    return result
