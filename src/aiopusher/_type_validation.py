"""Type validation utilities."""

from typing import Any, Union, get_args, get_origin

__all__ = ["validate_type"]


def validate_type(value: Any, type_hint: type):
    """Validate the type of a value. Raises TypeError if the type does not match.

    Args:
        value: The value to validate.
        type_hint: The type hint to validate against.

    Raises:
        TypeError: If the type of the value does not match the type hint.
    """
    if get_origin(type_hint) is Union:
        _validate_union_type(value, type_hint)
    elif not isinstance(value, type_hint):
        raise TypeError(f"Expected {type_hint}, got {type(value)}")


def _validate_union_type(value: Any, type_hint: Any):
    allowed_types = get_args(type_hint)
    if not isinstance(value, allowed_types):
        raise TypeError(f"Expected one of {allowed_types}, got {type(value)}")
