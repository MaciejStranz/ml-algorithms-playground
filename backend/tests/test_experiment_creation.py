import pytest
from unittest.mock import patch

from ml_api.models import Experiment


@pytest.mark.django_db
def test_create_experiment_success(
    auth_client, user, dataset_iris, algo_svm
):
    """
    Creating an experiment should:
    - create an Experiment row for the authenticated user,
    - call the ML runner (mocked here),
    - persist returned metrics/predictions,
    - finish with status=finished,
    - return 201.
    """

    runner_result = {
        "metrics": {"accuracy": 0.93},
        "predictions": {"y_true": [0, 1], "y_pred": [0, 1]},
    }

    payload = {
        "dataset": dataset_iris.id,
        "algorithm": algo_svm.id,
        "hyperparameters": {},
        "test_size": 0.3,
        "random_state": 42,
        "include_predictions": True,
        "include_probabilities": False,
    }

    with patch(
        "ml_api.views.run_experiment", return_value=runner_result
    ) as mocked_runner:
        res = auth_client.post("/api/experiments/", payload, format="json")

    assert res.status_code == 201

    mocked_runner.assert_called_once()

    # Assert DB state: one experiment created for this user
    exp = Experiment.objects.get(user=user, dataset=dataset_iris, algorithm=algo_svm)

    assert exp.status == "finished"
    assert exp.metrics == runner_result["metrics"]
    assert exp.predictions == runner_result["predictions"]

    assert exp.test_size == payload["test_size"]
    assert exp.random_state == payload["random_state"]
    assert exp.include_predictions == payload["include_predictions"]
    assert exp.include_probabilities == payload["include_probabilities"]


@pytest.mark.django_db
def test_create_experiment_error(
    auth_client, user, dataset_iris, algo_svm
):
    """
    If the ML runner raises ValueError, the endpoint should:
    - mark the created Experiment as failed,
    - return 400 with a readable error message.
    """

    payload = {
        "dataset": dataset_iris.id,
        "algorithm": algo_svm.id,
        "hyperparameters": {"random": "invalid"},
        "test_size": 0.3,
        "random_state": 42,
        "include_predictions": True,
        "include_probabilities": False,
    }

    with patch("ml_api.views.run_experiment", side_effect=ValueError("bad hyperparameters")):
        res = auth_client.post("/api/experiments/", payload, format="json")

    assert res.status_code == 400
    body = res.json()
    assert "detail" in body
    assert "bad hyperparameters" in body["detail"]

    # The record should exist and be marked as failed.
    exp = Experiment.objects.filter(user=user).order_by("-created_at").first()
    assert exp is not None
    assert exp.dataset_id == dataset_iris.id
    assert exp.algorithm_id == algo_svm.id
    assert exp.status == "failed"

    # On failure, we should not persist metrics/predictions from runner.
    assert exp.metrics == {}
    assert exp.predictions is None

