import pytest
from ml_api.models import Experiment

def test_experiment_detail_access_for_owner(auth_client, auth_client2, user, dataset_diabetes, algo_svm, make_experiment):
    exp_user1 = make_experiment(user=user, dataset=dataset_diabetes, algorithm=algo_svm, metrics={"accuracy": 0.9})

    res = auth_client.get(f"/api/experiments/{exp_user1.id}/")
    res_failed = auth_client2.get(f"/api/experiments/{exp_user1.id}/")

    assert res.status_code == 200
    assert exp_user1.id == res.json()["id"]
    assert res_failed.status_code == 404

@pytest.mark.django_db
def test_experiment_detail_delete_only_owner(auth_client, auth_client2, user, dataset_diabetes, algo_svm, make_experiment):
    exp_user1 = make_experiment(user=user, dataset=dataset_diabetes, algorithm=algo_svm, metrics={"accuracy": 0.9})

    res_failed = auth_client2.delete(f"/api/experiments/{exp_user1.id}/")

    assert res_failed.status_code == 404
    assert Experiment.objects.filter(id=exp_user1.id).exists()

    res = auth_client.delete(f"/api/experiments/{exp_user1.id}/")

    assert res.status_code == 204
    assert not Experiment.objects.filter(id=exp_user1.id).exists()

