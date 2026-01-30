import pytest

from ml_core.common.types import ParamType, TaskType
from ml_core.algorithms.hparam_specs import ALGORITHM_HPARAMS, get_hyperparameter_specs
from ml_core.common.hyperparameters import validate_value_against_spec


def test_registry_specs_are_consistent():
    """
    Contract test: hyperparameter specs are metadata used by backend and frontend.
    If this breaks, UI generation and validation will break.
    """
    for algo_name, specs in ALGORITHM_HPARAMS.items():
        assert isinstance(specs, list) and specs, f"{algo_name}: specs list is empty"

        seen_names = set()
        for s in specs:
            assert s.name, f"{algo_name}: spec.name is empty"
            assert s.name not in seen_names, f"{algo_name}: duplicate param name {s.name!r}"
            seen_names.add(s.name)

            # Bounds sanity
            if s.min is not None and s.max is not None:
                assert s.min <= s.max, f"{algo_name}.{s.name}: min > max"

            # Choices sanity
            if s.choices is not None:
                assert isinstance(s.choices, list) and len(s.choices) > 0, f"{algo_name}.{s.name}: choices empty"

            # Default sanity (only when default is not None)
            if s.default is not None:
                # validate_value_against_spec checks type/range/choices
                # Note: for ParamType.INT, a float default like 1.0 will pass "number" check,
                # which you may or may not want. If you want strict int, enforce separately.
                validate_value_against_spec(s, s.default)

def test_svm_epsilon_is_only_for_regression():
    """
    Contract test: SVM 'epsilon' is an SVR-only hyperparameter (regression).
    """
    regression_specs = get_hyperparameter_specs("svm", TaskType.REGRESSION)
    binary_specs = get_hyperparameter_specs("svm", TaskType.BINARY)
    multiclass_specs = get_hyperparameter_specs("svm", TaskType.MULTICLASS)

    assert any(s.name == "epsilon" for s in regression_specs)
    assert all(s.name != "epsilon" for s in binary_specs)
    assert all(s.name != "epsilon" for s in multiclass_specs)