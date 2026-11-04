import pytest

from hotel_booking import booking_cost, cancellation_refund, room_upgrade


@pytest.mark.parametrize(
    ("room", "nights", "guests", "peak", "expected"),
    [
        ("standard", 2, 2, False, 4000),
        ("standard", 2, 2, True, 5000),
        ("deluxe", 1, 3, False, 4000),
        ("standard", 7, 2, False, 12600),
        ("suite", 1, 2, False, 6000),
    ],
)
def test_booking_cost_valid_branches(room, nights, guests, peak, expected):
    assert booking_cost(room, nights, guests, peak) == expected


def test_booking_cost_unknown_room_branch():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("unknown", 1, 1, False)


def test_booking_cost_invalid_nights_branch():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 1, False)


@pytest.mark.parametrize(
    ("days_before", "is_member", "expected"),
    [
        (7, False, 1000),
        (6, False, 500),
        (1, False, 0),
        (6, True, 750),
        (1, True, 250),
    ],
)
def test_cancellation_refund_branches(days_before, is_member, expected):
    assert cancellation_refund(1000, days_before, is_member) == expected


def test_full_refund_returns_before_member_bonus():
    assert cancellation_refund(1000, 10, True) == 1000


def test_no_upgrade_when_no_rooms_are_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_receives_deluxe_upgrade():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_standard_non_member_receives_no_upgrade():
    assert room_upgrade("standard", False, 1) == "standard"


def test_deluxe_member_receives_suite_upgrade():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_deluxe_non_member_receives_no_upgrade():
    assert room_upgrade("deluxe", False, 1) == "deluxe"


def test_suite_does_not_receive_upgrade():
    assert room_upgrade("suite", True, 1) == "suite"
