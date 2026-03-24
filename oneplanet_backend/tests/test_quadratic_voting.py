"""Tests for the quadratic voting service layer."""

from oneplanet_backend.services.quadratic_voting import (
    quadratic_cost,
    tally_proposal,
    validate_weights,
)


# --- quadratic_cost ---
def test_cost_single_weight():
    assert quadratic_cost({"a": 3}) == 9.0


def test_cost_multiple_weights():
    assert quadratic_cost({"a": 3, "b": 1}) == 10.0


def test_cost_empty():
    assert quadratic_cost({}) == 0.0


def test_cost_floats():
    assert abs(quadratic_cost({"x": 1.5}) - 2.25) < 1e-9


def test_cost_zero_weights():
    assert quadratic_cost({"a": 0, "b": 0}) == 0.0


# --- validate_weights ---
def test_validate_valid():
    assert validate_weights({"a": 1, "b": 2}) == []


def test_validate_empty_dict():
    errors = validate_weights({})
    assert len(errors) == 1
    assert "non-empty" in errors[0]


def test_validate_not_dict():
    errors = validate_weights("not a dict")  # type: ignore[arg-type]
    assert len(errors) == 1


def test_validate_negative():
    errors = validate_weights({"a": -1})
    assert len(errors) == 1
    assert ">= 0" in errors[0]


def test_validate_non_numeric():
    errors = validate_weights({"a": "bad"})  # type: ignore[dict-item]
    assert len(errors) == 1
    assert "numeric" in errors[0]


def test_validate_mixed_errors():
    errors = validate_weights({"a": -1, "b": "x"})  # type: ignore[dict-item]
    assert len(errors) == 2


# --- tally_proposal ---
def test_tally_single_voter():
    assert tally_proposal([{"a": 3, "b": 1}]) == {"a": 3.0, "b": 1.0}


def test_tally_multiple_voters():
    result = tally_proposal([{"a": 3, "b": 1}, {"a": 1, "b": 2}])
    assert result == {"a": 4.0, "b": 3.0}


def test_tally_empty():
    assert tally_proposal([]) == {}


def test_tally_disjoint_choices():
    result = tally_proposal([{"a": 1}, {"b": 2}])
    assert result == {"a": 1.0, "b": 2.0}
