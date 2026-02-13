import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from ml_api.models import Dataset, Algorithm, Experiment, AlgorithmVariant

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    """
    Create a default user for permission/ownership tests
    """
    User = get_user_model()
    return User.objects.create_user(username="testuser", password="testpass123")


@pytest.fixture
def user2(db):
    """
    Secondary user useful for permission/ownership tests.
    """
    User = get_user_model()
    return User.objects.create_user(
        username="otheruser",
        password="otherpass123",
    )


@pytest.fixture
def auth_client(user):
    """
    API client already authenticated as `user`.
    """
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def auth_client2(user2):
    """
    API client already authenticated as `user2`.
    """
    client = APIClient()
    client.force_authenticate(user=user2)
    return client

@pytest.fixture
def dataset_iris(db):
    return Dataset.objects.create(
        code="iris",
        name="Iris",
        task="multiclass_classification",
        n_samples=150,
        n_features=4,
        n_classes=3,
        class_labels=["0", "1", "2"],
        feature_names=["f1", "f2", "f3", "f4"],
        target_name="class",
    )


@pytest.fixture
def dataset_diabetes(db):
    return Dataset.objects.create(
        code="diabetes",
        name="Diabetes",
        task="regression",
        n_samples=442,
        n_features=10,
        n_classes=None,
        class_labels=None,
        feature_names=None,
        target_name="target",
    )


@pytest.fixture
def algo_svm(db):
    return Algorithm.objects.create(
        code="svm",
        name="Support Vector Machine",
        kind="classical",
        description="SVM classifier/regressor."
    )

@pytest.fixture
def variant_svc(db, algo_svm):
    return AlgorithmVariant.objects.create(
        algorithm=algo_svm,
        code="svc",
        supported_tasks=["binary_classification", "multiclass_classification"],
        hyperparameter_specs=[{"name": "C", "type": "float", "default": 1.0}],
    )


@pytest.fixture
def variant_svr(db, algo_svm):
    return AlgorithmVariant.objects.create(
        algorithm=algo_svm,
        code="svr",
        supported_tasks=["regression"],
        hyperparameter_specs=[{"name": "epsilon", "type": "float", "default": 0.1}],
    )


@pytest.fixture
def make_experiment(db, variant_svc, variant_svr):
    """
    Factory fixture to create experiments with minimal boilerplate.
    Now supports AlgorithmVariant.
    """
    def _make(*, user, dataset, algorithm=None, algorithm_variant=None, **kwargs):
        # Backward compat: allow passing algorithm, but variant is the source of truth
        if algorithm_variant is None:
            if dataset.task == "regression":
                algorithm_variant = variant_svr
            else:
                algorithm_variant = variant_svc

        if algorithm is None:
            algorithm = algorithm_variant.algorithm

        defaults = dict(
            task=dataset.task,
            status="finished",
            hyperparameters={},
            metrics={},
            predictions=None,
            test_size=0.3,
            random_state=42,
            include_predictions=True,
            include_probabilities=False,
        )
        defaults.update(kwargs)

        return Experiment.objects.create(
            user=user,
            dataset=dataset,
            algorithm=algorithm,
            algorithm_variant=algorithm_variant,
            **defaults,
        )

    return _make
