import pytest

from ml_core.runner import RunConfig, run_experiment

from ml_core.algorithms.catalog import get_algorithm
from ml_core.common.types import TaskType
from ml_core.common.hyperparameters import validate_params_against_specs


def test_regression_variant_rejects_classification_only_param_C():
    algo = get_algorithm("regression")
    variant = algo.get_variant(TaskType.REGRESSION)  # LinearRegression
    specs_map = {s.name: s for s in variant.hyperparams}

    with pytest.raises(ValueError, match="not allowed"):
        validate_params_against_specs(specs_map, {"C": 1.0})


def test_runner_regression_classification_smoke():
    cfg = RunConfig(
        dataset_name="breast_cancer",
        algorithm_name="regression",
        hyperparams={"C": 1.0, "l1_ratio": 0.5, "fit_intercept": True},
        include_predictions=False,
        include_probabilities=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "accuracy" in result["metrics"]


def test_runner_regression_regression_smoke():
    cfg = RunConfig(
        dataset_name="diabetes",
        algorithm_name="regression",
        hyperparams={"fit_intercept": True},
        include_predictions=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "r2" in result["metrics"]
