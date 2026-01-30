from enum import Enum

class TaskType(str, Enum):
    BINARY = "binary_classification"
    MULTICLASS = "multiclass_classification"
    REGRESSION = "regression"

class TaskFamily(str, Enum):
    """
    Coarser task grouping used for algorithm variants and UI filtering.

    - BINARY/MULTICLASS -> CLASSIFICATION
    - REGRESSION -> REGRESSION
    """
    CLASSIFICATION = "classification"
    REGRESSION = "regression"


def task_family_from_task(task: TaskType) -> TaskFamily:
    """
    Map a concrete TaskType to a TaskFamily.
    """
    if task in (TaskType.BINARY, TaskType.MULTICLASS):
        return TaskFamily.CLASSIFICATION
    if task == TaskType.REGRESSION:
        return TaskFamily.REGRESSION
    raise ValueError(f"Unsupported TaskType: {task!r}")

class ParamType(str, Enum):
    """Generic type of a hyperparameter value."""
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    CHOICE = "choice"
    NUMBER_OR_STRING = "number_or_string"  # e.g. gamma: float or "scale"/"auto"
    INT_LIST = "int_list"