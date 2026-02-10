from rest_framework import serializers

from ml_api.models import Dataset, Algorithm, Experiment, AlgorithmVariant
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for managing users.
    """

    class Meta:
        model = User
        fields = ["id", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        print(validated_data)
        user = User.objects.create_user(**validated_data)
        return user


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


class AlgorithmVariantSerializer(serializers.ModelSerializer):
    """
    Serializer for specific variants of algorithms and hyperparameters associated with it.
    """

    algorithm = serializers.SerializerMethodField()

    class Meta:
        model = AlgorithmVariant
        fields = ["id", "code", "supported_tasks", "hyperparameter_specs", "algorithm"]

        def get_algorithm(self, obj):
            return {
                "id": obj.algorithm.id,
                "code": obj.algorithm.code,
                "name": obj.algorithm.name,
                "kind": obj.algorithm.kind,
            }


class AlgorithmVariantInlineSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlgorithmVariant
        fields = [
            "id",
            "code",
            "supported_tasks",
            "hyperparameter_specs",
        ]


class AlgorithmVariantCompactSerializer(serializers.ModelSerializer):
    algorithm = serializers.SerializerMethodField()

    class Meta:
        model = AlgorithmVariant
        fields = ["id", "code", "algorithm"]

    def get_algorithm(self, obj):
        return {
            "id": obj.algorithm.id,
            "code": obj.algorithm.code,
            "name": obj.algorithm.name,
        }


class AlgorithmSerializer(serializers.ModelSerializer):
    variants = AlgorithmVariantInlineSerializer(many=True, read_only=True)

    class Meta:
        model = Algorithm
        fields = [
            "id",
            "code",
            "name",
            "kind",
            "description",
            "variants",
        ]


class AlgorithmCompactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Algorithm
        fields = ["id", "code", "name", "kind"]


class ExperimentListSerializer(serializers.ModelSerializer):
    """
    Compact representation of an experiment for list views.

    Includes basic metadata, status and top-level metrics.
    """

    dataset = serializers.SerializerMethodField()
    algorithm_variant = AlgorithmVariantCompactSerializer(read_only=True)

    class Meta:
        model = Experiment
        fields = [
            "id",
            "dataset",
            "algorithm_variant",
            "task",
            "created_at",
            "status",
            "hyperparameters",
            "metrics",
        ]

    def get_dataset(self, obj):
        return {
            "id": obj.dataset.id,
            "name": obj.dataset.name,
        }


class ExperimentDetailSerializer(serializers.ModelSerializer):
    """
    Detailed experiment representation, including configuration and results.
    """

    dataset = DatasetSerializer(read_only=True)
    algorithm_variant = AlgorithmVariantSerializer(read_only=True)

    class Meta:
        model = Experiment
        fields = [
            "id",
            "dataset",
            "algorithm_variant",
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

    Uses foreign keys to Dataset and Algorithm_variant models via DRF relation fields.
    """

    # Foreign keys – DRF will resolve IDs to model instances automatically.
    dataset = serializers.PrimaryKeyRelatedField(queryset=Dataset.objects.all())
    algorithm_variant = serializers.PrimaryKeyRelatedField(
        queryset=AlgorithmVariant.objects.select_related("algorithm")
    )

    hyperparameters = serializers.DictField(
        child=serializers.JSONField(),
        required=False,
        help_text="Algorithm-variant-specific hyperparameters.",
    )

    test_size = serializers.FloatField(required=False, default=0.3)
    random_state = serializers.IntegerField(required=False, default=42)
    include_predictions = serializers.BooleanField(required=False, default=True)
    include_probabilities = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        dataset = attrs["dataset"]
        variant = attrs["algorithm_variant"]

        # Ensure user can't pick a variant that doesn't support dataset.task
        supported = variant.supported_tasks or []
        if dataset.task not in supported:
            raise serializers.ValidationError(
                {
                    "algorithm_variant": f"Variant {variant.code!r} does not support task {dataset.task!r}."
                }
            )

        return attrs
