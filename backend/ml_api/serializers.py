from rest_framework import serializers

from ml_api.models import Dataset, Algorithm, Experiment


class DatasetSerializer(serializers.ModelSerializer):
    """
    Serializer for dataset metadata.

    Exposes only read-only metadata fields; the actual data samples
    are loaded by ml_core and never stored in the database.
    """

    class Meta:
        model = Dataset
        fields = [
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
        ]


class AlgorithmSerializer(serializers.ModelSerializer):
    """
    Serializer for algorithm metadata and hyperparameter specifications.
    """

    class Meta:
        model = Algorithm
        fields = [
            "id",
            "code",
            "name",
            "kind",
            "description",
            "hyperparameter_specs",
        ]


class ExperimentListSerializer(serializers.ModelSerializer):
    """
    Compact representation of an experiment for list views.

    Includes basic metadata, status and top-level metrics.
    """

    dataset = DatasetSerializer(read_only=True)
    algorithm = AlgorithmSerializer(read_only=True)

    class Meta:
        model = Experiment
        fields = [
            "id",
            "dataset",
            "algorithm",
            "task",
            "created_at",
            "status",
            "metrics",
        ]


class ExperimentDetailSerializer(serializers.ModelSerializer):
    """
    Detailed experiment representation, including configuration and results.
    """

    dataset = DatasetSerializer(read_only=True)
    algorithm = AlgorithmSerializer(read_only=True)

    class Meta:
        model = Experiment
        fields = [
            "id",
            "dataset",
            "algorithm",
            "task",
            "created_at",
            "status",
            # configuration
            "hyperparameters",
            "test_size",
            "random_state",
            "include_predictions",
            "include_probabilities",
            # results
            "metrics",
            "predictions",
        ]


class ExperimentCreateSerializer(serializers.Serializer):
    """
    Input payload for creating a new experiment.

    The actual training is delegated to ml_core.runner.run_experiment.
    """

    dataset_id = serializers.IntegerField()
    algorithm_id = serializers.IntegerField()
    hyperparameters = serializers.DictField(
        child=serializers.JSONField(),
        required=False,
        help_text="Algorithm-specific hyperparameters.",
    )

    test_size = serializers.FloatField(required=False, default=0.3)
    random_state = serializers.IntegerField(required=False, default=42)
    include_predictions = serializers.BooleanField(required=False, default=True)
    include_probabilities = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        """
        Resolve dataset and algorithm instances and perform basic validation.

        More advanced validation (e.g. hyperparameter schema) is performed
        inside ml_core via validate_hyperparameters and run_experiment.
        """
        try:
            dataset = Dataset.objects.get(id=attrs["dataset_id"])
        except Dataset.DoesNotExist:
            raise serializers.ValidationError({"dataset_id": "Dataset not found."})

        try:
            algorithm = Algorithm.objects.get(id=attrs["algorithm_id"])
        except Algorithm.DoesNotExist:
            raise serializers.ValidationError({"algorithm_id": "Algorithm not found."})

        attrs["dataset"] = dataset
        attrs["algorithm"] = algorithm
        attrs["hyperparameters"] = attrs.get("hyperparameters") or {}
        return attrs