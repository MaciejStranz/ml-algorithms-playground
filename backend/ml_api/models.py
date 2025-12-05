from django.db import models
from django.conf import settings


class Dataset(models.Model):
    code = models.CharField(max_length=50, unique=True)  # np. "iris", "wine", "sinx"
    name = models.CharField(max_length=100)
    task = models.CharField(max_length=20)  # "binary" | "multiclass" | "regression"
    n_samples = models.IntegerField()
    n_features = models.IntegerField()
    n_classes = models.IntegerField(null=True, blank=True)
    class_labels = models.JSONField(null=True, blank=True)     # ["setosa", ...]
    feature_names = models.JSONField(null=True, blank=True)    # ["sepal length", ...]
    target_name = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.name} ({self.code})"
    
class Algorithm(models.Model):
    """
    Metadata for algorithms available in the system.

    The 'code' field must match the identifier used inside ml_core
    (e.g. "svm", "random_forest", "xgboost", "logistic", "mlp").
    """

    code = models.CharField(max_length=50, unique=True)   # e.g. "svm", "random_forest", "mlp"
    name = models.CharField(max_length=100)               # Human-readable name

    kind = models.CharField(
        max_length=20,
        choices=[
            ("classical", "Classical (sklearn/xgboost)"),
            ("deep", "Deep (PyTorch)"),
        ],
    )

    # Full hyperparameter specification as JSON-friendly structures from ml_core
    # This is expected to be a list of dicts, not a plain dict.
    hyperparameter_specs = models.JSONField(default=list)

    # Optional algorithm description shown in the UI or exposed via API
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"
    

class Experiment(models.Model):
    """
    Single training + evaluation run performed by a user.

    This links together:
    - the user who triggered the experiment,
    - the chosen dataset,
    - the chosen algorithm,
    - the configuration used for the run (hyperparameters, split, options),
    - the resulting metrics and predictions.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="experiments",
    )

    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE)
    algorithm = models.ForeignKey(Algorithm, on_delete=models.CASCADE)

    # Cached task type, copied from Dataset.task for convenience
    task = models.CharField(max_length=20)  # "binary" | "multiclass" | "regression"

    created_at = models.DateTimeField(auto_now_add=True)

    # Run configuration (aligned with RunConfig in ml_core.runner)
    hyperparameters = models.JSONField(default=dict)
    test_size = models.FloatField(default=0.3)
    random_state = models.IntegerField(default=42)
    include_predictions = models.BooleanField(default=True)
    include_probabilities = models.BooleanField(default=False)

    # Results coming from run_experiment(...)
    metrics = models.JSONField(default=dict)
    predictions = models.JSONField(null=True, blank=True)

    # Later: training_log, visualizations, etc.
    # training_log = models.JSONField(null=True, blank=True)
    # visualizations = models.JSONField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        default="finished",
        choices=[
            ("running", "Running"),
            ("finished", "Finished"),
            ("failed", "Failed"),
        ],
    )

    # Optional path to a saved model artifact (for future /predict endpoints)
    model_path = models.CharField(max_length=512, null=True, blank=True)

    def __str__(self) -> str:
        return f"Experiment #{self.id} by {self.user} on {self.dataset.code} ({self.algorithm.code})"
