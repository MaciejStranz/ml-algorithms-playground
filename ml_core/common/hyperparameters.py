# ml_core/common/hyperparams.py

from __future__ import annotations

from dataclasses import dataclass, asdict
from enum import Enum
from typing import Any, Dict, List, Optional

from .types import TaskType, ParamType


@dataclass
class HyperparameterSpec:
    """
    Specification of a single hyperparameter exposed by an algorithm.

    This is used by:
    - the ML core, to know what parameters exist and how they should look,
    - the backend, to serialize this to JSON and validate user input,
    - the frontend, to render appropriate controls (slider, dropdown, etc.).
    """

    # Name as expected by the underlying library (e.g. sklearn/XGBoost).
    name: str

    # Human-readable label for UI (e.g. "Regularization C").
    display_name: str

    # Generic type of the parameter (affects how it is rendered and validated).
    type: ParamType

    # Default value used when the user does not override this parameter.
    default: Any

    # Short description for tooltips / docs in the UI.
    description: str

    # Optional lower/upper bounds (for INT/FLOAT/NUMBER_OR_STRING when numeric).
    min: Optional[float] = None
    max: Optional[float] = None

    # For CHOICE or STRING/NUMBER_OR_STRING with restricted set of string values.
    choices: Optional[List[Any]] = None

    # If set, this parameter is only applicable for the given tasks.
    # If None, it is considered valid for all tasks.
    applicable_tasks: Optional[List[TaskType]] = None

    # Whether this parameter should be shown in the basic UI
    # (vs. "advanced" / "expert" section).
    advanced: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the spec to a plain dict suitable for JSON serialization.
        Enums are converted to their `.value`.
        """
        data = asdict(self)
        data["type"] = self.type.value
        if self.applicable_tasks is not None:
            data["applicable_tasks"] = [t.value for t in self.applicable_tasks]
        return data


def specs_to_dict_list(specs: List[HyperparameterSpec]) -> List[Dict[str, Any]]:
    """Helper to convert a list of specs into a list of dicts for JSON."""
    return [spec.to_dict() for spec in specs]


# ---------- Generic single-parameter validation (no cross-parameter deps) ----------

def validate_value_against_spec(spec: HyperparameterSpec, value: Any) -> None:
    """
    Validate a single value against a HyperparameterSpec.

    This does NOT check cross-parameter dependencies – only type, range, and choices.
    Raises ValueError on failure.
    """
    t = spec.type

    if t in (ParamType.INT, ParamType.FLOAT):
        if not isinstance(value, (int, float)):
            raise ValueError(
                f"Parameter {spec.name!r} must be a number (int/float), "
                f"but got {type(value).__name__}."
            )
        if spec.min is not None and value < spec.min:
            raise ValueError(
                f"Parameter {spec.name!r}={value} is below the minimum {spec.min}."
            )
        if spec.max is not None and value > spec.max:
            raise ValueError(
                f"Parameter {spec.name!r}={value} is above the maximum {spec.max}."
            )

    elif t is ParamType.BOOL:
        if not isinstance(value, bool):
            raise ValueError(
                f"Parameter {spec.name!r} must be a boolean, "
                f"but got {type(value).__name__}."
            )

    elif t is ParamType.CHOICE:
        if spec.choices is not None and value not in spec.choices:
            allowed = ", ".join(map(str, spec.choices))
            raise ValueError(
                f"Parameter {spec.name!r} must be one of: {allowed}. Got: {value!r}"
            )

    elif t is ParamType.STRING:
        if not isinstance(value, str):
            raise ValueError(
                f"Parameter {spec.name!r} must be a string, "
                f"but got {type(value).__name__}."
            )
        if spec.choices is not None and value not in spec.choices:
            allowed = ", ".join(map(str, spec.choices))
            raise ValueError(
                f"Parameter {spec.name!r} must be one of: {allowed}. Got: {value!r}"
            )

    elif t is ParamType.NUMBER_OR_STRING:
        # Example: gamma: either float in [min, max] OR one of choices ("scale", "auto").
        if isinstance(value, (int, float)):
            if spec.min is not None and value < spec.min:
                raise ValueError(
                    f"Parameter {spec.name!r}={value} is below the minimum {spec.min}."
                )
            if spec.max is not None and value > spec.max:
                raise ValueError(
                    f"Parameter {spec.name!r}={value} is above the maximum {spec.max}."
                )
        elif isinstance(value, str):
            if spec.choices is not None and value not in spec.choices:
                allowed = ", ".join(map(str, spec.choices))
                raise ValueError(
                    f"Parameter {spec.name!r} must be one of: {allowed} or a numeric "
                    f"value. Got: {value!r}"
                )
        else:
            raise ValueError(
                f"Parameter {spec.name!r} must be either a number or string, "
                f"but got {type(value).__name__}."
            )

    else:
        # Fallback – if a new type is added and not handled
        raise ValueError(f"Unsupported ParamType {t} for parameter {spec.name!r}.")


def validate_params_against_specs(
    specs: Dict[str, HyperparameterSpec],
    user_params: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Validate user-provided hyperparameters against a mapping of name -> HyperparameterSpec.

    - Unknown parameters are rejected.
    - Values are validated w.r.t. type, range, choices.

    Returns a sanitized dict.
    Raises ValueError on any validation issue.

    NOTE: This function does NOT enforce cross-parameter dependencies
    on purpose. Things like 'gamma' vs 'kernel' are left to the underlying
    library (e.g. sklearn SVC/SVR), which already knows how to handle them.
    """
    validated: Dict[str, Any] = {}

    for name, value in user_params.items():
        if name not in specs:
            available = ", ".join(sorted(specs.keys()))
            raise ValueError(
                f"Parameter {name!r} is not allowed for this algorithm. "
                f"Available parameters: {available}"
            )

        spec = specs[name]
        validate_value_against_spec(spec, value)
        validated[name] = value

    return validated
