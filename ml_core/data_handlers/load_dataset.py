from dataclasses import dataclass
from typing import Callable, Tuple

import numpy as np
from sklearn.datasets import load_iris, load_wine, load_breast_cancer
from sklearn.model_selection import train_test_split

from .metadata import DatasetMeta, TaskType


@dataclass
class Dataset:
    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    meta: DatasetMeta

def _load_iris() -> Tuple[Tuple[np.ndarray, np.ndarray], DatasetMeta]:
    bunch = load_iris()
    meta = DatasetMeta(
        id="iris",
        name="Iris",
        task=TaskType.MULTICLASS,
        n_samples=bunch.data.shape[0],
        n_features=bunch.data.shape[1],
        n_classes=len(set(bunch.target)),
        class_labels=list(bunch.target_names),
        feature_names=list(bunch.feature_names),
        target_name="species",
    )
    return (bunch.data, bunch.target), meta


def _load_wine() -> Tuple[Tuple[np.ndarray, np.ndarray], DatasetMeta]:
    bunch = load_wine()
    meta = DatasetMeta(
        id="wine",
        name="Wine",
        task=TaskType.MULTICLASS,
        n_samples=bunch.data.shape[0],
        n_features=bunch.data.shape[1],
        n_classes=len(set(bunch.target)),
        class_labels=list(bunch.target_names),
        feature_names=list(bunch.feature_names),
        target_name="class",
    )
    return (bunch.data, bunch.target), meta

def _load_breast_cancer() -> Tuple[Tuple[np.ndarray, np.ndarray], DatasetMeta]:
    bunch = load_breast_cancer()
    meta = DatasetMeta(
        id="breast_cancer",
        name="Breast Cancer",
        task=TaskType.BINARY,
        n_samples=bunch.data.shape[0],
        n_features=bunch.data.shape[1],
        n_classes=len(set(bunch.target)),
        class_labels=list(bunch.target_names),
        feature_names=list(bunch.feature_names),
        target_name="class",
    )
    return (bunch.data, bunch.target), meta


DATASET_LOADERS: dict[str, Callable[[], Tuple[Tuple[np.ndarray, np.ndarray], DatasetMeta]]] = {
    "iris": _load_iris,
    "wine": _load_wine,
    "breast_cancer": _load_breast_cancer,
}


def load_data(
    name: str,
    test_size: float = 0.3,
    random_state: int = 42,
) -> Dataset:
    try:
        (X, y), meta = DATASET_LOADERS[name]()
    except KeyError:
        available = ", ".join(DATASET_LOADERS.keys())
        raise ValueError(
            f"Unsupported dataset name: {name!r}. Available: {available}"
        ) from None

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    return Dataset(
        X_train=X_train,
        X_test=X_test,
        y_train=y_train,
        y_test=y_test,
        meta=meta,
    )
