from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class TaskType(str, Enum):
    BINARY = "binary_classification"
    MULTICLASS = "multiclass_classification"
    REGRESSION = "regression"


@dataclass
class DatasetMeta:
    id: str                 # np. "iris"
    name: str               # Friendly name: "Iris"
    task: TaskType
    n_samples: int
    n_features: int

    # target
    n_classes: Optional[int] = None
    class_labels: Optional[List[str]] = None
    
    # some extra info
    feature_names: Optional[List[str]] = None
    target_name: Optional[str] = None
