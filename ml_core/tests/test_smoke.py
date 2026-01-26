import pytest

from ml_core.runner import RunConfig, run_experiment


def test_run_experiment_fails_fast_for_unknown_entities():
    """
    Smoke test:
    - ensures ml_core is importable
    - ensures runner validates config and fails fast for unknown dataset/algorithm
    """
    cfg = RunConfig(
        dataset_name="__does_not_exist__",
        algorithm_name="__does_not_exist__",
        hyperparams={},
        test_size=0.3,
        random_state=42,
        include_predictions=False,
        include_probabilities=False,
    )

    with pytest.raises(ValueError):
        run_experiment(cfg)
