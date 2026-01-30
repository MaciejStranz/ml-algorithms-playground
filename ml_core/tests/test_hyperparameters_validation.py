import pytest

from ml_core.common.types import ParamType
from ml_core.common.hyperparameters import HyperparameterSpec, validate_params_against_specs


def test_validate_params_against_specs_rejects_unknown_param():
    specs = {
        "C": HyperparameterSpec(
            name="C",
            display_name="C",
            type=ParamType.FLOAT,
            default=1.0,
            description="Regularization strength.",
            min=0.0001,
            max=10000,
        )
    }

    with pytest.raises(ValueError, match=r"not allowed|Available parameters"):
        validate_params_against_specs(specs, {"gamma": 0.1})


def test_validate_params_against_specs_rejects_out_of_range_value():
    specs = {
        "C": HyperparameterSpec(
            name="C",
            display_name="C",
            type=ParamType.FLOAT,
            default=1.0,
            description="Regularization strength.",
            min=0.0001,
            max=10000,
        )
    }

    with pytest.raises(ValueError, match=r"below the minimum"):
        validate_params_against_specs(specs, {"C": 0.0})


def test_validate_params_against_specs_accepts_valid_values():
    specs = {
        "C": HyperparameterSpec(
            name="C",
            display_name="C",
            type=ParamType.FLOAT,
            default=1.0,
            description="Regularization strength.",
            min=0.0001,
            max=10000,
        ),
        "kernel": HyperparameterSpec(
            name="kernel",
            display_name="Kernel",
            type=ParamType.CHOICE,
            default="rbf",
            description="SVM kernel.",
            choices=["linear", "rbf", "poly"],
        ),
        "fit_intercept": HyperparameterSpec(
            name="fit_intercept",
            display_name="Fit intercept",
            type=ParamType.BOOL,
            default=True,
            description="Whether to fit intercept.",
        ),
        "hidden_dims": HyperparameterSpec(
            name="hidden_dims",
            display_name="Hidden dims",
            type=ParamType.INT_LIST,
            default=[64, 64],
            description="MLP architecture.",
        ),
        "gamma": HyperparameterSpec(
            name="gamma",
            display_name="Gamma",
            type=ParamType.NUMBER_OR_STRING,
            default="scale",
            description="Kernel coefficient.",
            min=1e-6,
            max=1000,
            choices=["scale", "auto"],
        ),
    }

    user_params = {
        "C": 1.5,
        "kernel": "rbf",
        "fit_intercept": False,
        "hidden_dims": [128, 64],
        "gamma": "scale",
    }

    validated = validate_params_against_specs(specs, user_params)

    # Contract: validated dict matches input for accepted values
    assert validated == user_params

def test_number_or_string_rejects_invalid_numeric_and_invalid_string():
    specs = {
        "gamma": HyperparameterSpec(
            name="gamma",
            display_name="Gamma",
            type=ParamType.NUMBER_OR_STRING,
            default="scale",
            description="Kernel coefficient.",
            min=0.001,
            max=10.0,
            choices=["scale", "auto"],
        )
    }

    # Case 1: numeric value below min
    with pytest.raises(ValueError, match=r"below the minimum"):
        validate_params_against_specs(specs, {"gamma": 0.0001})

    # Case 2: string not in choices
    with pytest.raises(ValueError, match=r"must be one of"):
        validate_params_against_specs(specs, {"gamma": "invalid"})

