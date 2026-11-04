import pytest

from hotel_booking import booking_cost, cancellation_refund, room_upgrade


def test_standard_booking_cost():
    assert booking_cost("standard", 2, 2, False) == 4000


def test_unknown_room_is_rejected():
    with pytest.raises(ValueError, match="unknown room"):
        booking_cost("presidential", 2, 2, False)


def test_invalid_nights_are_rejected():
    with pytest.raises(ValueError, match="invalid nights"):
        booking_cost("standard", 0, 2, False)


def test_peak_season_rate():
    assert booking_cost("standard", 1, 2, True) == 2500


def test_extra_guest_charge():
    assert booking_cost("standard", 2, 3, False) == 5000


def test_weekly_booking_discount():
    assert booking_cost("standard", 7, 2, False) == 12600


def test_peak_season_extra_guests_and_weekly_discount():
    assert booking_cost("deluxe", 7, 3, True) == 30713


def test_full_refund():
    assert cancellation_refund(1000, 10, False) == 1000


def test_full_refund_for_member_is_not_changed():
    assert cancellation_refund(1000, 7, True) == 1000


def test_half_refund():
    assert cancellation_refund(1000, 5, False) == 500


def test_half_refund_plus_member_bonus():
    assert cancellation_refund(1000, 5, True) == 750


def test_no_refund():
    assert cancellation_refund(1000, 1, False) == 0


def test_member_refund_bonus_when_cancelling_late():
    assert cancellation_refund(1000, 1, True) == 250


def test_no_upgrade_when_no_rooms_are_free():
    assert room_upgrade("standard", True, 0) == "standard"


def test_standard_member_upgrades_to_deluxe():
    assert room_upgrade("standard", True, 1) == "deluxe"


def test_deluxe_member_upgrades_to_suite():
    assert room_upgrade("deluxe", True, 1) == "suite"


def test_non_member_does_not_get_upgrade():
    assert room_upgrade("standard", False, 1) == "standard"


def test_suite_does_not_upgrade_further():
    assert room_upgrade("suite", True, 1) == "suite"
