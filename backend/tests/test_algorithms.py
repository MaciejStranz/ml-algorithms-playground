import pytest


@pytest.mark.django_db
def test_algorithms_list_shape_ok(auth_client, algo_svm, variant_svc):
    """
    Algorithms list returns items matching AlgorithmSerializer fields
    (after refactor: variants instead of hyperparameter_specs).
    """
    res = auth_client.get("/api/algorithms/")
    assert res.status_code == 200

    data = res.json()
    items = data if isinstance(data, list) else data.get("results", [])
    assert isinstance(items, list)
    assert len(items) >= 1

    item = items[0]
    expected_keys = {"id", "code", "name", "kind", "description", "variants"}
    assert expected_keys.issubset(item.keys())

    assert isinstance(item["id"], int)
    assert isinstance(item["code"], str)
    assert isinstance(item["name"], str)
    assert isinstance(item["kind"], str)
    assert isinstance(item["description"], str)

    variants = item["variants"]
    assert isinstance(variants, list)

    # If there are variants, validate minimal shape of a variant.
    if variants:
        v = variants[0]
        v_keys = {"id", "code", "supported_tasks", "hyperparameter_specs"}
        assert v_keys.issubset(v.keys())

        assert isinstance(v["id"], int)
        assert isinstance(v["code"], str)
        assert isinstance(v["supported_tasks"], list)
        assert isinstance(v["hyperparameter_specs"], list)

        # If there are specs, validate minimal shape of one spec.
        if v["hyperparameter_specs"]:
            spec = v["hyperparameter_specs"][0]
            spec_keys = {"name", "type", "default"}
            assert spec_keys.issubset(spec.keys())
            assert isinstance(spec["name"], str)
            assert isinstance(spec["type"], str)
            # default can be many JSON types -> don't assert exact type
