import pytest


@pytest.mark.django_db
def test_algorithm_variants_requires_auth(api_client, variant_svc):
    res = api_client.get("/api/algorithm-variants/")
    assert res.status_code in (401, 403)  # 401 typical for DRF, 403 possible depending on settings


@pytest.mark.django_db
def test_algorithm_variants_list_ok(auth_client, variant_svc):
    res = auth_client.get("/api/algorithm-variants/")
    assert res.status_code == 200

    data = res.json()
    assert isinstance(data, list)
    assert len(data) >= 1

    item = data[0]
    # minimal API contract
    assert "id" in item
    assert "code" in item
    assert "supported_tasks" in item
    assert "hyperparameter_specs" in item


@pytest.mark.django_db
def test_algorithm_variants_filter_by_task(auth_client, variant_svc, variant_svr):
    # regression -> should return only SVR (based on fixture supported_tasks)
    res = auth_client.get("/api/algorithm-variants/?task=regression")
    assert res.status_code == 200

    data = res.json()
    codes = [v["code"] for v in data]

    assert "svr" in codes
    assert "svc" not in codes

    # multiclass_classification -> should return SVC, not SVR
    res2 = auth_client.get("/api/algorithm-variants/?task=multiclass_classification")
    assert res2.status_code == 200

    data2 = res2.json()
    codes2 = [v["code"] for v in data2]

    assert "svc" in codes2
    assert "svr" not in codes2
