from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, List, Optional, Sequence, Tuple, Dict, Any

import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset

from ml_core.common.types import TaskType


def _get_device(device: Optional[str] = None) -> torch.device:
    if device is not None:
        return torch.device(device)
    return torch.device("cuda" if torch.cuda.is_available() else "cpu")


def _make_activation(name: str) -> nn.Module:
    name = name.lower()
    if name == "relu":
        return nn.ReLU()
    if name == "tanh":
        return nn.Tanh()
    if name == "gelu":
        return nn.GELU()
    raise ValueError(f"Unsupported activation: {name!r}")


class _MLP(nn.Module):
    """
    Simple fully-connected MLP with configurable hidden layers and activation.
    """

    def __init__(
        self,
        input_dim: int,
        hidden_dims: Sequence[int],
        output_dim: int,
        activation: str = "relu",
        dropout: float = 0.0,
    ) -> None:
        super().__init__()

        layers: List[nn.Module] = []
        in_dim = input_dim
        act = _make_activation(activation)

        for h in hidden_dims:
            layers.append(nn.Linear(in_dim, h))
            layers.append(act)
            if dropout > 0.0:
                layers.append(nn.Dropout(dropout))
            in_dim = h

        layers.append(nn.Linear(in_dim, output_dim))
        self.net = nn.Sequential(*layers)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.net(x)


@dataclass
class _TrainingConfig:
    lr: float = 1e-3
    batch_size: int = 64
    max_epochs: int = 100
    weight_decay: float = 0.0
    verbose: bool = False


class MLPClassifier:
    """
    Torch-based MLP classifier with a sklearn-like API.

    - Uses CrossEntropyLoss.
    - Number of input features is inferred from X on first fit.
    - Number of classes is inferred from y on first fit.
    - For binary classification, it still uses K=2 classes with softmax.
    """

    def __init__(
        self,
        hidden_dims: Sequence[int] = (64, 64),
        activation: str = "relu",
        dropout: float = 0.0,
        lr: float = 1e-3,
        batch_size: int = 64,
        max_epochs: int = 100,
        weight_decay: float = 0.0,
        device: Optional[str] = None,
        random_state: Optional[int] = None,
        verbose: bool = False,
    ) -> None:
        self.hidden_dims = hidden_dims
        self.activation = activation
        self.dropout = dropout
        self.cfg = _TrainingConfig(
            lr=lr,
            batch_size=batch_size,
            max_epochs=max_epochs,
            weight_decay=weight_decay,
            verbose=verbose,
        )
        self._device = _get_device(device)
        self._model: Optional[_MLP] = None
        self._n_features: Optional[int] = None
        self._n_classes: Optional[int] = None
        self._random_state = random_state

        if random_state is not None:
            torch.manual_seed(random_state)
            np.random.seed(random_state)

    def _build_model(self, input_dim: int, n_classes: int) -> None:
        self._model = _MLP(
            input_dim=input_dim,
            hidden_dims=self.hidden_dims,
            output_dim=n_classes,
            activation=self.activation,
            dropout=self.dropout,
        ).to(self._device)
        self._n_features = input_dim
        self._n_classes = n_classes

    def fit(self, X: np.ndarray, y: np.ndarray) -> "MLPClassifier":
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y, dtype=np.int64)

        if X.ndim != 2:
            raise ValueError(f"X must be 2D (n_samples, n_features), got shape {X.shape}")
        if y.ndim != 1:
            raise ValueError(f"y must be 1D (n_samples,), got shape {y.shape}")
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples.")

        n_samples, n_features = X.shape
        classes = np.unique(y)
        n_classes = int(classes.max()) + 1  # assume labels are 0..K-1

        if self._model is None:
            self._build_model(n_features, n_classes)
        else:
            if self._n_features != n_features:
                raise ValueError(
                    f"Model was built for {self._n_features} features, "
                    f"but got X with {n_features} features."
                )

        assert self._model is not None  # for type checkers
        model = self._model
        model.train()

        X_tensor = torch.from_numpy(X).to(self._device)
        y_tensor = torch.from_numpy(y).to(self._device)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(
            dataset,
            batch_size=self.cfg.batch_size,
            shuffle=True,
            drop_last=False,
        )

        criterion = nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=self.cfg.lr,
            weight_decay=self.cfg.weight_decay,
        )

        for epoch in range(self.cfg.max_epochs):
            epoch_loss = 0.0
            for xb, yb in loader:
                optimizer.zero_grad()
                logits = model(xb)
                loss = criterion(logits, yb)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * xb.size(0)

            if self.cfg.verbose:
                avg_loss = epoch_loss / n_samples
                print(f"[MLPClassifier] Epoch {epoch+1}/{self.cfg.max_epochs} - loss={avg_loss:.4f}")

        return self

    def _predict_logits(self, X: np.ndarray) -> torch.Tensor:
        if self._model is None:
            raise RuntimeError("Model is not fitted yet. Call `fit` first.")

        X = np.asarray(X, dtype=np.float32)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D (n_samples, n_features), got shape {X.shape}")

        if self._n_features is not None and X.shape[1] != self._n_features:
            raise ValueError(
                f"Model was built for {self._n_features} features, "
                f"but got X with {X.shape[1]} features."
            )

        self._model.eval()
        with torch.no_grad():
            X_tensor = torch.from_numpy(X).to(self._device)
            logits = self._model(X_tensor)
        return logits

    def predict(self, X: np.ndarray) -> np.ndarray:
        logits = self._predict_logits(X)
        preds = torch.argmax(logits, dim=1)
        return preds.cpu().numpy()

    def predict_proba(self, X: np.ndarray) -> np.ndarray:
        logits = self._predict_logits(X)
        probs = torch.softmax(logits, dim=1)
        return probs.cpu().numpy()


class MLPRegressor:
    """
    Torch-based MLP regressor with a sklearn-like API.

    - Uses MSELoss.
    - Number of input features is inferred from X on first fit.
    - Output is a single scalar per sample.
    """

    def __init__(
        self,
        hidden_dims: Sequence[int] = (64, 64),
        activation: str = "relu",
        dropout: float = 0.0,
        lr: float = 1e-3,
        batch_size: int = 64,
        max_epochs: int = 100,
        weight_decay: float = 0.0,
        device: Optional[str] = None,
        random_state: Optional[int] = None,
        verbose: bool = False,
    ) -> None:
        self.hidden_dims = hidden_dims
        self.activation = activation
        self.dropout = dropout
        self.cfg = _TrainingConfig(
            lr=lr,
            batch_size=batch_size,
            max_epochs=max_epochs,
            weight_decay=weight_decay,
            verbose=verbose,
        )
        self._device = _get_device(device)
        self._model: Optional[_MLP] = None
        self._n_features: Optional[int] = None
        self._random_state = random_state

        if random_state is not None:
            torch.manual_seed(random_state)
            np.random.seed(random_state)

    def _build_model(self, input_dim: int) -> None:
        self._model = _MLP(
            input_dim=input_dim,
            hidden_dims=self.hidden_dims,
            output_dim=1,
            activation=self.activation,
            dropout=self.dropout,
        ).to(self._device)
        self._n_features = input_dim

    def fit(self, X: np.ndarray, y: np.ndarray) -> "MLPRegressor":
        X = np.asarray(X, dtype=np.float32)
        y = np.asarray(y, dtype=np.float32)

        if X.ndim != 2:
            raise ValueError(f"X must be 2D (n_samples, n_features), got shape {X.shape}")
        if y.ndim not in (1, 2):
            raise ValueError(f"y must be 1D or 2D, got shape {y.shape}")
        if y.ndim == 2 and y.shape[1] != 1:
            raise ValueError("For regression, y must be (n_samples,) or (n_samples, 1).")
        if X.shape[0] != y.shape[0]:
            raise ValueError("X and y must have the same number of samples.")

        n_samples, n_features = X.shape
        y = y.reshape(-1, 1)

        if self._model is None:
            self._build_model(n_features)
        else:
            if self._n_features != n_features:
                raise ValueError(
                    f"Model was built for {self._n_features} features, "
                    f"but got X with {n_features} features."
                )

        assert self._model is not None
        model = self._model
        model.train()

        X_tensor = torch.from_numpy(X).to(self._device)
        y_tensor = torch.from_numpy(y).to(self._device)

        dataset = TensorDataset(X_tensor, y_tensor)
        loader = DataLoader(
            dataset,
            batch_size=self.cfg.batch_size,
            shuffle=True,
            drop_last=False,
        )

        criterion = nn.MSELoss()
        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=self.cfg.lr,
            weight_decay=self.cfg.weight_decay,
        )

        for epoch in range(self.cfg.max_epochs):
            epoch_loss = 0.0
            for xb, yb in loader:
                optimizer.zero_grad()
                pred = model(xb)
                loss = criterion(pred, yb)
                loss.backward()
                optimizer.step()
                epoch_loss += loss.item() * xb.size(0)

            if self.cfg.verbose:
                avg_loss = epoch_loss / n_samples
                print(f"[MLPRegressor] Epoch {epoch+1}/{self.cfg.max_epochs} - loss={avg_loss:.4f}")

        return self

    def predict(self, X: np.ndarray) -> np.ndarray:
        if self._model is None:
            raise RuntimeError("Model is not fitted yet. Call `fit` first.")

        X = np.asarray(X, dtype=np.float32)
        if X.ndim != 2:
            raise ValueError(f"X must be 2D (n_samples, n_features), got shape {X.shape}")

        if self._n_features is not None and X.shape[1] != self._n_features:
            raise ValueError(
                f"Model was built for {self._n_features} features, "
                f"but got X with {X.shape[1]} features."
            )

        self._model.eval()
        with torch.no_grad():
            X_tensor = torch.from_numpy(X).to(self._device)
            preds = self._model(X_tensor)
        return preds.cpu().numpy().reshape(-1)
    

def _mlp_factory(task: TaskType, params: Dict[str, Any] | None):
    params = dict(params or {})

    if "hidden_dims" not in params:
        params["hidden_dims"] = [64, 64]

    if task in (TaskType.BINARY, TaskType.MULTICLASS):
        return MLPClassifier(**params)
    elif task == TaskType.REGRESSION:
        return MLPRegressor(**params)
    else:
        raise ValueError(f"MLP: unsupported task type {task!r}")


_DEEP_MODEL_FACTORIES: Dict[str, Any] = {
    "mlp": _mlp_factory,
}


def get_deep_model(
    name: str,
    task: TaskType,
    params: Dict[str, Any] | None = None,
):
    """
    Return a deep model instance for the given algorithm name and task.

    Parameters
    ----------
    name:
        Algorithm identifier, e.g. "mlp".
    task:
        TaskType (BINARY, MULTICLASS, REGRESSION).
    params:
        Hyperparameters to pass to the underlying model constructor.
        For MLP this may include:
        - hidden_dims (string '64,64' or list/tuple of ints),
        - activation,
        - dropout,
        - lr,
        - batch_size,
        - max_epochs,
        - weight_decay,
        - device, random_state, verbose (if you choose to expose them).

    Raises
    ------
    ValueError:
        If the algorithm name is unknown or the task is unsupported.
    """
    try:
        factory = _DEEP_MODEL_FACTORIES[name]
    except KeyError:
        available = ", ".join(sorted(_DEEP_MODEL_FACTORIES.keys()))
        raise ValueError(
            f"Unknown deep algorithm {name!r}. Available: {available}"
        ) from None

    return factory(task, params)
