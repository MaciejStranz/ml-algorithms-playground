from ml_core.algorithms.catalog import get_algorithm
from ml_core.common.types import TaskType
from ml_core.algorithms.deep.mlp import MLPClassifier
from ml_core.runner import RunConfig, run_experiment

def test_mlp_classification_variant_builds_classifier():
    algo = get_algorithm("mlp")
    variant = algo.get_variant(TaskType.MULTICLASS)
    model = variant.factory({"max_epochs": 1})
    assert isinstance(model, MLPClassifier)

def test_runner_mlp_smoke_regression():
    cfg = RunConfig(
        dataset_name="diabetes",
        algorithm_name="mlp",
        hyperparams={"max_epochs": 100, "batch_size": 32},
        test_size=0.2,
        random_state=0,
        include_predictions=False,
    )
    result = run_experiment(cfg)
    assert "metrics" in result
    assert "r2" in result["metrics"]

def test_runner_mlp_smoke_classification():
    cfg = RunConfig(
        dataset_name="wine",
        algorithm_name="mlp",
        hyperparams={"max_epochs": 100, "batch_size": 32},
        test_size=0.2,
        random_state=0,
        include_predictions=False,
    )
    result = run_experiment(cfg)
    assert "metrics" in result
    assert "accuracy" in result["metrics"]
