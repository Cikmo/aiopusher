# pylint: disable=missing-module-docstring
# pylint: disable=missing-function-docstring

from typing import Union

import pytest

from aiopusher import _type_validation


def test_validate_type_with_matching_types():
    _type_validation.validate_type(10, int)
    _type_validation.validate_type("test", str)
    _type_validation.validate_type([1, 2, 3], list)


def test_validate_type_with_unmatching_types():
    with pytest.raises(TypeError):
        _type_validation.validate_type(10, str)

    with pytest.raises(TypeError):
        _type_validation.validate_type("test", int)

    with pytest.raises(TypeError):
        _type_validation.validate_type([1, 2, 3], str)


def test_validate_type_with_matching_union_types():
    type_hint = Union[int, str]

    _type_validation.validate_type(10, type_hint)
    _type_validation.validate_type("test", type_hint)


def test_validate_type_with_unmatching_union_types():
    with pytest.raises(TypeError):
        _type_validation.validate_type([1, 2, 3], Union[int, str])


def test_validate_type_with_non_type_hint():
    with pytest.raises(TypeError):
        _type_validation.validate_type(10, "not a type hint")  # type: ignore
