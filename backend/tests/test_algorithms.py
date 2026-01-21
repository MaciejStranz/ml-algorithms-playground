import pytest


@pytest.mark.django_db
def test_algorithms_list_shape_ok(algo_svm, auth_client):
    """
    Algorithms list returns items matching AlgorithmSerializer fields
    """
    res = auth_client.get("/api/algorithms/")

    assert res.status_code == 200

    data = res.json()
    items = data if isinstance(data, list) else data.get("results", [])
    assert isinstance(items, list)
    assert len(items) >= 1

    item = items[0]
    expected_keys = {
        "id",
        "code",
        "name",
        "kind",
        "description",
        "hyperparameter_specs",
    }
    assert expected_keys.issubset(item.keys())

    assert isinstance(item["id"], int)
    assert isinstance(item["code"], str)
    assert isinstance(item["name"], str)
    assert isinstance(item["kind"], str)
    assert isinstance(item["description"], str)

    specs = item["hyperparameter_specs"]
    assert isinstance(specs, list)

    # If there are specs, validating the minimal shape of one of them.
    if specs:
        spec = specs[0]
        spec_keys = {"name", "type", "default", "applicable_tasks"}
        assert spec_keys.issubset(spec.keys())

        assert isinstance(spec["name"], str)
        assert isinstance(spec["type"], str)
        # default can be many types (null/number/string/list), so not asserting type
        assert isinstance(spec["applicable_tasks"], list)
