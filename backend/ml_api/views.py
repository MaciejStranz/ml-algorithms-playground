from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import ValidationError
from rest_framework import generics
from django.contrib.auth.models import User

from ml_api.models import Dataset, Algorithm, Experiment
from ml_api.serializers import (
    UserSerializer,
    DatasetSerializer,
    AlgorithmSerializer,
    ExperimentListSerializer,
    ExperimentDetailSerializer,
    ExperimentCreateSerializer,
)

from ml_core.runner import RunConfig, run_experiment


class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class DatasetViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for listing and inspecting available datasets.

    These entries are synchronized from ml_core via a management command
    and represent metadata only (no raw samples in the database).
    """

    queryset = Dataset.objects.all().order_by("name")
    serializer_class = DatasetSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Optional filtering by task, e.g. /api/datasets/?task=classification.
        """
        qs = super().get_queryset()
        task = self.request.query_params.get("task")
        if task:
            qs = qs.filter(task=task)
        return qs


class AlgorithmViewSet(ReadOnlyModelViewSet):
    """
    Read-only API for listing algorithms and their hyperparameter specs.
    """

    queryset = Algorithm.objects.all().order_by("name")
    serializer_class = AlgorithmSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Optional filtering by kind, e.g. /api/algorithms/?kind=classical or ?kind=deep.
        """
        qs = super().get_queryset()
        kind = self.request.query_params.get("kind")
        if kind:
            qs = qs.filter(kind=kind)
        return qs


class ExperimentViewSet(ModelViewSet):
    """
    Full CRUD API for user experiments.

    - list:   returns experiments of the authenticated user (summary view),
    - create: triggers a training + evaluation run via ml_core.runner,
    - retrieve: returns full details of a single experiment.
    """

    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Limit experiments to the current user and order by creation time.
        """
        return (
            Experiment.objects.filter(user=self.request.user)
            .select_related("dataset", "algorithm")
            .order_by("-created_at")
        )

    def get_serializer_class(self):
        """
        Use different serializers for list, detail and create operations.
        """
        if self.action == "list":
            return ExperimentListSerializer
        if self.action == "retrieve":
            return ExperimentDetailSerializer
        if self.action == "create":
            return ExperimentCreateSerializer
        return ExperimentDetailSerializer

    def perform_create(self, serializer):
        """
        Create an Experiment, run training + evaluation via ml_core, and
        persist the results in the database.

        Currently synchronous; can be moved to a background worker later.
        """
        user = self.request.user
        data = serializer.validated_data

        dataset = data["dataset"]          # already a Dataset instance
        algorithm = data["algorithm"]      # already an Algorithm instance
        hyperparams = data["hyperparameters"]
        test_size = data.get("test_size", 0.3)
        random_state = data.get("random_state", 42)
        include_predictions = data.get("include_predictions", True)
        include_probabilities = data.get("include_probabilities", False)

        # 1. Create Experiment record with 'running' status
        experiment = Experiment.objects.create(
            user=user,
            dataset=dataset,
            algorithm=algorithm,
            task=dataset.task,
            hyperparameters=hyperparams,
            test_size=test_size,
            random_state=random_state,
            include_predictions=include_predictions,
            include_probabilities=include_probabilities,
            status="running",
        )

        # 2. Build RunConfig from model state
        config = RunConfig(
            dataset_name=dataset.code,
            algorithm_name=algorithm.code,
            hyperparams=hyperparams,
            test_size=test_size,
            random_state=random_state,
            include_predictions=include_predictions,
            include_probabilities=include_probabilities,
        )

        try:
            result = run_experiment(config)
        except ValueError as e:
            experiment.status = "failed"
            experiment.save(update_fields=["status"])
            raise ValidationError({"detail": str(e)})
        except Exception as e:
            experiment.status = "failed"
            experiment.save(update_fields=["status"])
            raise ValidationError({"detail": f"Experiment failed: {e}"})

        # 3. Persist results
        experiment.metrics = result.get("metrics", {})
        experiment.predictions = result.get("predictions")
        experiment.status = "finished"
        experiment.save()

        # 4. Return full detail representation
        serializer.instance = experiment



