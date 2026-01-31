import pytest

from ml_core.runner import RunConfig, run_experiment

from ml_core.algorithms.catalog import get_algorithm
from ml_core.common.types import TaskFamily
from ml_core.common.hyperparameters import validate_params_against_specs


def test_xgb_validation_rejects_value_above_max():
    algo = get_algorithm("xgboost")
    variant = algo.get_variant(TaskFamily.CLASSIFICATION)
    specs_map = {s.name: s for s in variant.hyperparams}

    with pytest.raises(ValueError, match="learning_rate"):
        validate_params_against_specs(specs_map, {"learning_rate": 2.0})  # max=1.0



def test_runner_xgboost_classification_smoke():
    cfg = RunConfig(
        dataset_name="iris",
        algorithm_name="xgboost",
        hyperparams={"n_estimators": 10, "max_depth": 3, "learning_rate": 0.3},
        include_predictions=False,
        include_probabilities=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "accuracy" in result["metrics"]


def test_runner_xgboost_regression_smoke():
    cfg = RunConfig(
        dataset_name="diabetes",
        algorithm_name="xgboost",
        hyperparams={"n_estimators": 10, "max_depth": 3, "learning_rate": 0.3},
        include_predictions=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "r2" in result["metrics"]
