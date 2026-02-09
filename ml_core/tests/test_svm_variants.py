import pytest
import numbers
from sklearn.datasets import make_classification, make_regression

from ml_core.algorithms.catalog import get_algorithm
from ml_core.common.types import TaskType, task_family_from_task
from ml_core.common.hyperparameters import validate_params_against_specs
from ml_core.runner import RunConfig, run_experiment


def _validate_variant_params(algorithm_code: str, task: TaskType, params: dict) -> dict:
    """
    Helper that validates params against the correct algorithm variant
    """
    algo = get_algorithm(algorithm_code)
    variant = algo.get_variant(task)

    specs_map = {s.name: s for s in variant.hyperparams}
    return validate_params_against_specs(specs_map, params)


def test_svm_classification_rejects_epsilon():
    """
    SVM classification variant is implemented using SVC,
    so SVR-only hyperparameter 'epsilon' must not be allowed.
    """
    with pytest.raises(ValueError) as exc:
        _validate_variant_params(
            algorithm_code="svm",
            task=TaskType.MULTICLASS,
            params={"epsilon": 0.1},
        )

    # We assert message content to ensure it fails for the right reason.
    assert "not allowed" in str(exc.value).lower()
    assert "epsilon" in str(exc.value).lower()


def test_svm_regression_accepts_epsilon_and_model_can_fit():
    """
    SVM regression variant is implemented using SVR,
    so 'epsilon' should be allowed and the model should be buildable & trainable.
    """
    validated = _validate_variant_params(
        algorithm_code="svm",
        task=TaskType.REGRESSION,
        params={"epsilon": 0.2, "C": 1.5},
    )
    assert validated["epsilon"] == 0.2
    assert validated["C"] == 1.5

    # Build model via registry and smoke-test fit/predict.
    algo = get_algorithm("svm")
    variant = algo.get_variant(TaskType.REGRESSION)
    model = variant.factory(validated)

    X, y = make_regression(n_samples=40, n_features=4, noise=0.1, random_state=123)
    model.fit(X, y)
    preds = model.predict(X)

    assert len(preds) == len(y)


def test_svm_classification_model_can_fit_and_predict():
    """
    Ensure classification variant builds a model that trains and predicts.
    This is a light smoke test to verify the factory returns a usable estimator.
    """
    validated = _validate_variant_params(
        algorithm_code="svm",
        task=TaskType.BINARY,
        params={"C": 1.0, "kernel": "rbf"},
    )

    algo = get_algorithm("svm")
    variant = algo.get_variant(TaskType.BINARY)
    model = variant.factory(validated)

    X, y = make_classification(
        n_samples=60,
        n_features=6,
        n_informative=4,
        n_redundant=0,
        random_state=123,
    )
    model.fit(X, y)
    preds = model.predict(X)

    assert len(preds) == len(y)

def test_run_experiment_contract_classification():
    """
    Contract test for ml_core.runner.run_experiment:

    - returns a dict with "metrics" and (optionally) "predictions"
    - classification metrics include "accuracy"
    - when include_predictions=True -> predictions include y_true, y_pred
    - when include_probabilities=True (classification) -> predictions include y_proba
    - predictions lengths are consistent
    """

    # Use a fast/classical algorithm entry that supports classification
    config = RunConfig(
        dataset_name="iris",
        algorithm_name="svm",
        hyperparams={},
        test_size=0.3,
        random_state=42,
        include_predictions=True,
        include_probabilities=True,
    )

    result = run_experiment(config)

    assert isinstance(result, dict)

    # Metrics contract
    assert "metrics" in result
    metrics = result["metrics"]
    assert isinstance(metrics, dict)

    assert "accuracy" in metrics
    acc = metrics["accuracy"]
    assert isinstance(acc, numbers.Real)
    assert 0.0 <= float(acc) <= 1.0

    # Predictions contract
    assert "predictions" in result
    preds = result["predictions"]
    assert isinstance(preds, dict)

    assert "y_true" in preds
    assert "y_pred" in preds
    y_true = preds["y_true"]
    y_pred = preds["y_pred"]

    assert hasattr(y_true, "__len__")
    assert hasattr(y_pred, "__len__")
    assert len(y_true) == len(y_pred)
    assert len(y_true) > 0

    # Probabilities contract (classification only)
    assert "y_proba" in preds
    y_proba = preds["y_proba"]
    assert hasattr(y_proba, "__len__")
    assert len(y_proba) == len(y_true)


def test_runner_svm_regression_smoke():
    cfg = RunConfig(
        dataset_name="diabetes",
        algorithm_name="svm",
        hyperparams={"kernel":"rbf"},
        include_predictions=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "r2" in result["metrics"]
