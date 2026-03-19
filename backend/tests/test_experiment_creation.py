import pytest
from unittest.mock import patch

from ml_api.models import Experiment


@pytest.mark.django_db
def test_experiments_create_requires_auth(dataset_iris, variant_svc, api_client):
    """
    Create endpoint must require authentication.
    """
    payload = {
        "dataset": dataset_iris.id,
        "algorithm_variant": variant_svc.id,
        "hyperparameters": {},
        "test_size": 0.3,
        "random_state": 42,
        "include_predictions": True,
        "include_probabilities": False,
    }

    res = api_client.post("/api/experiments/", payload, format="json")
    assert res.status_code == 401


@pytest.mark.django_db
def test_create_experiment_success(auth_client, user, dataset_iris, algo_svm, variant_svc):
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
        "algorithm_variant": variant_svc.id,
        "hyperparameters": {},
        "test_size": 0.3,
        "random_state": 42,
        "include_predictions": True,
        "include_probabilities": False,
    }

    with patch("ml_api.views.run_experiment", return_value=runner_result) as mocked_runner:
        res = auth_client.post("/api/experiments/", payload, format="json")

    assert res.status_code == 201
    mocked_runner.assert_called_once()

    exp = Experiment.objects.get(
        user=user,
        dataset=dataset_iris,
        algorithm_variant=variant_svc,
    )

    assert exp.status == "finished"
    assert exp.metrics == runner_result["metrics"]
    assert exp.predictions == runner_result["predictions"]

    assert exp.test_size == payload["test_size"]
    assert exp.random_state == payload["random_state"]
    assert exp.include_predictions == payload["include_predictions"]
    assert exp.include_probabilities == payload["include_probabilities"]


@pytest.mark.django_db
def test_create_experiment_error(auth_client, user, dataset_iris, algo_svm, variant_svc):
    """
    If the ML runner raises ValueError, the endpoint should:
    - mark the created Experiment as failed,
    - return 400 with a readable error message.
    """
    payload = {
        "dataset": dataset_iris.id,
        "algorithm_variant": variant_svc.id,
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

    exp = Experiment.objects.filter(user=user).order_by("-created_at").first()
    assert exp is not None
    assert exp.dataset_id == dataset_iris.id
    assert exp.algorithm_variant_id == variant_svc.id

    assert exp.status == "failed"
    assert exp.metrics == {}
    assert exp.predictions is None


@pytest.mark.django_db
def test_experiments_create_invalid_fk_ids_returns_400(auth_client):
    """
    Invalid dataset/algorithm_variant ids should return 400 with field errors.
    """
    payload = {
        "dataset": 999999,
        "algorithm_variant": 888888,
        "hyperparameters": {},
        "test_size": 0.3,
        "random_state": 42,
        "include_predictions": True,
        "include_probabilities": False,
    }

    res = auth_client.post("/api/experiments/", payload, format="json")
    assert res.status_code == 400

    data = res.json()
    assert ("dataset" in data) or ("algorithm_variant" in data)

    if "dataset" in data:
        assert isinstance(data["dataset"], list) and len(data["dataset"]) > 0
    if "algorithm_variant" in data:
        assert isinstance(data["algorithm_variant"], list) and len(data["algorithm_variant"]) > 0
