
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterable, Optional, Dict

import numpy as np
from sklearn.metrics import (
    classification_report,
    mean_absolute_error,
    mean_squared_error,
    r2_score,
)

from common.types import TaskType


@dataclass
class EvaluationReport:
    y_true: Iterable[Any]
    y_pred: Iterable[Any]
    task: TaskType
    target_names: Optional[Iterable[str]] = None

    # ---------------------------------------
    #  Public API
    # ---------------------------------------

    def summary(self) -> Dict[str, Any]:
        """
        Zwraca metryki jako słownik (dict).
        Dla klasyfikacji -> classification_report(output_dict=True)
        Dla regresji     -> {mae, mse, rmse, r2}
        """
        if self.task in (TaskType.BINARY, TaskType.MULTICLASS):
            return classification_report(self.y_true, self.y_pred, output_dict=True)
        elif self.task == TaskType.REGRESSION:
            return self._regression_summary()
        else:
            raise ValueError(f"Unsupported task type: {self.task}")

    def report_str(self) -> str:
        """
        Zwraca tekstowy raport.
        """
        if self.task in (TaskType.BINARY, TaskType.MULTICLASS):
            return classification_report(self.y_true, self.y_pred)
        elif self.task == TaskType.REGRESSION:
            return self._regression_report_str()
        else:
            raise ValueError(f"Unsupported task type: {self.task}")

    def _regression_summary(self) -> Dict[str, float]:
        mse = mean_squared_error(self.y_true, self.y_pred)
        mae = mean_absolute_error(self.y_true, self.y_pred)
        rmse = float(np.sqrt(mse))
        r2 = r2_score(self.y_true, self.y_pred)

        return {
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "r2": r2,
        }

    def _regression_report_str(self) -> str:
        metrics = self._regression_summary()

        return (
            "Regression Report\n"
            "-----------------------------\n"
            f"MAE : {metrics['mae']:.4f}\n"
            f"MSE : {metrics['mse']:.4f}\n"
            f"RMSE: {metrics['rmse']:.4f}\n"
            f"R²  : {metrics['r2']:.4f}\n"
        )