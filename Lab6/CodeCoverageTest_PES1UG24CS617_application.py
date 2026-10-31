import pytest

from amusement_park_ride_access import (
    process_ride_admissions,
    inspect_safety_restraints
)


def patron(height=150, warning=False, child=False):
    return {
        "height_cm": height,
        "health_warning": warning,
        "is_child": child
    }


def group(ride="family", patrons=None, open_=True, fast=False):
    return {
        "is_open": open_,
        "ride_type": ride,
        "has_fast_lane": fast,
        "patrons": patrons or []
    }


def test_invalid_input_and_group_skips():
    with pytest.raises(ValueError):
        process_ride_admissions("invalid", 5)

    with pytest.raises(ValueError):
        process_ride_admissions([], -1)

    result = process_ride_admissions(
        [group(open_=False), group(ride="unknown")],
        5
    )

    assert result["status"] == "ZERO_ADMISSIONS"


def test_ticket_types_and_patron_outcomes():
    groups = [
        group(
            "roller_coaster",
            [
                patron(0),
                patron(150),
                patron(150, warning=True),
                patron(150)
            ]
        ),
        group(
            "water_ride",
            [
                patron(150, warning=True),
                patron(100),
                patron(150, child=True),
                patron(150)
            ]
        ),
        group(
            "family",
            [
                patron(150, child=True),
                patron(150)
            ],
            fast=True
        )
    ]

    result = process_ride_admissions(groups, 5)

    assert result == {
        "total_revenue": 49.8,
        "status": "COMPLETED"
    }


def test_result_statuses():
    result = process_ride_admissions(
        [group("unknown") for _ in range(5)],
        0
    )
    assert result["status"] == "SAFETY_AUDIT"

    result = process_ride_admissions(
        [group("family", [patron(100)])],
        0
    )
    assert result["status"] == "ZERO_ADMISSIONS"

    result = process_ride_admissions(
        [group("family", [patron()])],
        0
    )
    assert result["status"] == "COMPLETED"


def test_restraint_results():
    assert inspect_safety_restraints([]) == "NO_DATA"

    assert inspect_safety_restraints([[1]]) == "SAFE"

    assert inspect_safety_restraints([[0, 0]]) == "EMERGENCY_LOCK"