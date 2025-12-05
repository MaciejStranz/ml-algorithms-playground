from django.db import models

# Create your models here.


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
