"""
Quadratic Voting service – pure business logic, no HTTP/DB concerns.

Quadratic voting lets participants express intensity of preference.
Cost grows quadratically: voting with weight w costs w² credits.
"""

from __future__ import annotations


def quadratic_cost(weights: dict[str, int | float]) -> float:
    """Calculate total quadratic cost for a set of vote weights.

    >>> quadratic_cost({"a": 3, "b": 1})
    10.0
    >>> quadratic_cost({})
    0.0
    """
    return sum(w * w for w in weights.values())


def validate_weights(weights: dict[str, int | float]) -> list[str]:
    """Return a list of validation error messages (empty = valid).

    Rules:
    - weights must be a non-empty dict
    - all values must be numeric and >= 0
    """
    errors: list[str] = []
    if not isinstance(weights, dict) or not weights:
        errors.append("vote_weights must be a non-empty dict.")
        return errors
    for key, val in weights.items():
        if not isinstance(val, int | float):
            errors.append(f"Weight '{key}' must be numeric, got {type(val).__name__}.")
        elif val < 0:
            errors.append(f"Weight '{key}' must be >= 0, got {val}.")
    return errors


def tally_proposal(votes: list[dict[str, int | float]]) -> dict[str, float]:
    """Aggregate multiple vote-weight dicts for the same proposal.

    Returns total weight per choice across all voters.

    >>> tally_proposal([{"a": 3, "b": 1}, {"a": 1, "b": 2}])
    {'a': 4.0, 'b': 3.0}
    """
    totals: dict[str, float] = {}
    for weights in votes:
        for choice, w in weights.items():
            totals[choice] = totals.get(choice, 0.0) + w
    return totals
