import pytest

@pytest.mark.django_db
def test_datasets_list_shape_ok(dataset_iris, auth_client):
    """
    Datasets list returns items matching DatasetSerializer fields.
    This protects the frontend from accidental serializer changes.
    """
    res = auth_client.get("/api/datasets/")

    assert res.status_code == 200

    data = res.json()
    items = data 
    assert isinstance(items, list)
    assert len(items) >= 1

    item = items[0]
    expected_keys = {
        "id",
        "code",
        "name",
        "task",
        "n_samples",
        "n_features",
        "n_classes",
        "class_labels",
        "feature_names",
        "target_name",
    }

    assert expected_keys.issubset(item.keys())

    # Basic type sanity checks 
    assert isinstance(item["id"], int)
    assert isinstance(item["code"], str)
    assert isinstance(item["name"], str)
    assert isinstance(item["task"], str)
