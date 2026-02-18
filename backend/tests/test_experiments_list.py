import pytest
from django.utils import timezone
from datetime import timedelta


def test_experiments_list_requires_auth(api_client):
    res = api_client.get("/api/experiments/")

    assert res.status_code == 401


def test_experiments_list_only_current_user(
    auth_client, auth_client2, user, user2, dataset_iris, make_experiment
):
    exp_user1 = make_experiment(
        user=user, dataset=dataset_iris, metrics={"accuracy": 0.9}
    )
    exp_user2 = make_experiment(
        user=user2, dataset=dataset_iris, metrics={"accuracy": 0.8}
    )

    res1 = auth_client.get("/api/experiments/")
    assert res1.status_code == 200
    ids1 = [item["id"] for item in res1.json()]
    assert exp_user1.id in ids1
    assert exp_user2.id not in ids1

    res2 = auth_client2.get("/api/experiments/")
    assert res2.status_code == 200
    ids2 = [item["id"] for item in res2.json()]
    assert exp_user2.id in ids2
    assert exp_user1.id not in ids2


@pytest.mark.django_db
def test_experiments_list_ordering_desc(
    auth_client, user, dataset_iris, dataset_diabetes, make_experiment
):
    exp1 = make_experiment(
        user=user, dataset=dataset_iris, metrics={"accuracy": 0.9}
    )
    exp2 = make_experiment(
        user=user,
        dataset=dataset_diabetes,
        metrics={"accuracy": 0.8},
    )

    now = timezone.now()
    type(exp1).objects.filter(id=exp1.id).update(created_at=now - timedelta(days=1))
    type(exp2).objects.filter(id=exp2.id).update(created_at=now)

    res = auth_client.get("/api/experiments/")
    assert res.status_code == 200

    ids = [item["id"] for item in res.json()]
    assert ids[:2] == [exp2.id, exp1.id]
