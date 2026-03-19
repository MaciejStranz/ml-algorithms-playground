import pytest

from ml_core.runner import RunConfig, run_experiment
from ml_core.common.types import TaskType
from ml_core.common.hyperparameters import validate_params_against_specs
from ml_core.algorithms.catalog import get_algorithm


def test_rf_variant_validation_rejects_invalid_choice():
    algo = get_algorithm("random_forest")

    variant = algo.get_variant(TaskType.BINARY)

    specs_map = {s.name: s for s in variant.hyperparams}

    with pytest.raises(ValueError, match="max_features"):
        validate_params_against_specs(specs_map, {"max_features": "auto"})


def test_runner_random_forest_classification_smoke():
    cfg = RunConfig(
        dataset_name="iris",
        algorithm_name="random_forest",
        hyperparams={"n_estimators": 10, "max_features": "sqrt", "max_depth" : None},
        include_predictions=False,
        include_probabilities=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "accuracy" in result["metrics"]

def test_runner_random_forest_regression_smoke():
    cfg = RunConfig(
        dataset_name="diabetes",
        algorithm_name="random_forest",
        hyperparams={"n_estimators": 10, "max_features": "sqrt"},
        include_predictions=False,
    )

    result = run_experiment(cfg)
    assert "metrics" in result
    assert "r2" in result["metrics"]
