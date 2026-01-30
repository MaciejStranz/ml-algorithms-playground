import numbers

import pytest

from ml_core.runner import RunConfig, run_experiment


def test_run_experiment_contract_classification_with_predictions_and_proba():
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
        algorithm_name="regression",
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

def test_run_experiment_contract_regression_without_probabilities():
    """
    Contract test for regression experiments:

    - metrics include r2
    - accuracy is NOT present
    - predictions include y_true/y_pred
    - probabilities are NOT returned
    """

    config = RunConfig(
        dataset_name="sinus",   # regression dataset
        algorithm_name="regression",
        hyperparams={},
        test_size=0.3,
        random_state=42,
        include_predictions=True,
        include_probabilities=True,  # should be ignored for regression
    )

    result = run_experiment(config)

    assert isinstance(result, dict)

    # Metrics
    metrics = result["metrics"]
    assert isinstance(metrics, dict)

    assert "r2" in metrics
    assert isinstance(metrics["r2"], float)

    assert "accuracy" not in metrics

    # Predictions
    preds = result["predictions"]

    assert "y_true" in preds
    assert "y_pred" in preds

    y_true = preds["y_true"]
    y_pred = preds["y_pred"]

    assert len(y_true) == len(y_pred)
    assert len(y_true) > 0

    # Regression should NOT expose probabilities
    assert "y_proba" not in preds


def test_run_experiment_contract_classification_without_predictions_and_proba():
    """
    Contract test for ml_core.runner.run_experiment:

    - returns only a dict with "metrics" 
    - classification metrics include "accuracy"
    - when include_predictions=False and include_probabilities=False -> no predictions in result
    """

    # Use a fast/classical algorithm entry that supports classification
    config = RunConfig(
        dataset_name="iris",
        algorithm_name="regression",
        hyperparams={},
        test_size=0.3,
        random_state=42,
        include_predictions=False,
        include_probabilities=False,
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

    # Predictions not in results
    assert "predictions" not in result