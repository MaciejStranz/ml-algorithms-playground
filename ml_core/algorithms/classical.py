# ml_core/algorithms/classical.py
from typing import Any, Dict
from sklearn.svm import SVC, SVR
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from common.types import TaskType
from xgboost import XGBClassifier, XGBRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


from common.types import TaskType


def _svm_factory(task: TaskType, params: Dict[str, Any] | None):
    params = params or {}
    if task in (TaskType.BINARY, TaskType.MULTICLASS):
        base_model = SVC(**{"probability": True, **params})
    elif task == TaskType.REGRESSION:
        base_model = SVR(**params)
    else:
        raise ValueError(f"SVM: unsupported task {task}")
    return make_pipeline(StandardScaler(), base_model)


def _rf_factory(task: TaskType, params: Dict[str, Any] | None):
    params = params or {}
    if task in (TaskType.BINARY, TaskType.MULTICLASS):
        return RandomForestClassifier(**params)
    elif task == TaskType.REGRESSION:
        return RandomForestRegressor(**params)
    else:
        raise ValueError(f"RandomForest: unsupported task {task}")


def _xgb_factory(task: TaskType, params: Dict[str, Any] | None):
    params = params or {}
    if task in (TaskType.BINARY, TaskType.MULTICLASS):
        return XGBClassifier(**params)
    elif task == TaskType.REGRESSION:
        return XGBRegressor(**params)
    else:
        raise ValueError(f"XGBoost: unsupported task {task}")


def _logreg_factory(task: TaskType, params: Dict[str, Any] | None):
    params = params or {}
    if task in (TaskType.BINARY, TaskType.MULTICLASS):
        return LogisticRegression(**{"max_iter": 1000, **params})
    elif task == TaskType.REGRESSION:
        return LinearRegression(**params)
    else:
        raise ValueError(f"Logistic/Linear: unsupported task {task}")


_MODEL_FACTORIES = {
    "svm": _svm_factory,
    "random_forest": _rf_factory,
    "xgboost": _xgb_factory,
    "logistic": _logreg_factory,
}


def get_classical_model(
    name: str,
    task: TaskType,
    params: Dict[str, Any] | None = None,
):
    try:
        factory = _MODEL_FACTORIES[name]
    except KeyError:
        available = ", ".join(_MODEL_FACTORIES.keys())
        raise ValueError(f"Unknown algorithm {name!r}. Available: {available}") from None

    return factory(task, params)
