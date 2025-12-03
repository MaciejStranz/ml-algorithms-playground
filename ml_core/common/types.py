from enum import Enum

class TaskType(str, Enum):
    BINARY = "binary_classification"
    MULTICLASS = "multiclass_classification"
    REGRESSION = "regression"

class ParamType(str, Enum):
    """Generic type of a hyperparameter value."""
    INT = "int"
    FLOAT = "float"
    BOOL = "bool"
    STRING = "string"
    CHOICE = "choice"
    NUMBER_OR_STRING = "number_or_string"  # e.g. gamma: float or "scale"/"auto"