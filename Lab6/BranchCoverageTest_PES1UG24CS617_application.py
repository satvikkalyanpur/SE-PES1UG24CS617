import pytest

from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


def p(height=150, warning=False, child=False):
    return {
        "height_cm": height,
        "health_warning": warning,
        "is_child": child
    }


def g(ride="family", patrons=None, open_=True, fast=False):
    return {
        "is_open": open_,
        "ride_type": ride,
        "has_fast_lane": fast,
        "patrons": patrons or []
    }


def test_invalid_inputs():
    with pytest.raises(ValueError):
        process_ride_admissions("not a list", 5)

    with pytest.raises(ValueError):
        process_ride_admissions([], -1)


def test_group_and_ride_branches():
    assert process_ride_admissions(
        [], 5
    )["status"] == "ZERO_ADMISSIONS"

    assert process_ride_admissions(
        [g(open_=False)], 5
    )["status"] == "ZERO_ADMISSIONS"

    assert process_ride_admissions(
        [g(ride="unknown")], 5
    )["status"] == "ZERO_ADMISSIONS"

    result = process_ride_admissions(
        [
            g("roller_coaster", [p()]),
            g("water_ride", [p()]),
            g("family", [p()])
        ],
        0
    )

    assert result["total_revenue"] == 53.0


def test_patron_decisions_and_fast_lane():
    result = process_ride_admissions(
        [
            g(
                "family",
                [
                    p(0),
                    p(100),
                    p(150, child=True),
                    p(150)
                ],
                fast=True
            )
        ],
        5
    )

    assert result == {
        "total_revenue": 21.0,
        "status": "COMPLETED"
    }

    result = process_ride_admissions(
        [
            g(
                "water_ride",
                [
                    p(150, warning=True),
                    p(150)
                ]
            )
        ],
        0
    )

    assert result["total_revenue"] == 18.0

    result = process_ride_admissions(
        [
            g(
                "roller_coaster",
                [
                    p(150),
                    p(150, warning=True),
                    p(150)
                ]
            )
        ],
        0
    )

    assert result["total_revenue"] == 0.0


def test_safety_audit_and_zero_and_completed():
    assert process_ride_admissions(
        [g("unknown") for _ in range(5)],
        0
    )["status"] == "SAFETY_AUDIT"

    assert process_ride_admissions(
        [g("family", [p(100)])],
        0
    )["status"] == "ZERO_ADMISSIONS"

    assert process_ride_admissions(
        [g("family", [p()])],
        0
    )["status"] == "COMPLETED"


def test_restraint_branches():
    assert inspect_safety_restraints(None) == "NO_DATA"

    assert inspect_safety_restraints([]) == "NO_DATA"

    assert inspect_safety_restraints([[]]) == "SAFE"

    assert inspect_safety_restraints([[1]]) == "SAFE"

    assert inspect_safety_restraints([[0, 1, 0]]) == "SAFE"

    assert inspect_safety_restraints([[0, 0]]) == "EMERGENCY_LOCK"