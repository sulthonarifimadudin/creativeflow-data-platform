import pandas as pd

from etl.quality import (
    check_duplicates,
    check_required_columns,
    check_positive_values,
    check_reference,
    check_date_order,
    check_allowed_values,
    check_payment_after_booking
)


def test_duplicate_detection():
    df = pd.DataFrame({
        "client_id": ["CLI001", "CLI001", "CLI002"]
    })

    result = check_duplicates(df, "client_id")

    assert result is False


def test_no_duplicate():
    df = pd.DataFrame({
        "client_id": ["CLI001", "CLI002", "CLI003"]
    })

    result = check_duplicates(df, "client_id")

    assert result is True


def test_required_column_null():
    df = pd.DataFrame({
        "booking_id": ["BOOK001", None]
    })

    result = check_required_columns(
        df,
        ["booking_id"]
    )

    assert result is False


def test_positive_amount():
    df = pd.DataFrame({
        "amount": [1000000, 500000, -100]
    })

    result = check_positive_values(
        df,
        "amount"
    )

    assert result is False

def test_valid_reference():
    bookings = pd.DataFrame({
        "client_id": ["CLI001", "CLI002"]
    })

    clients = pd.DataFrame({
        "client_id": ["CLI001", "CLI002", "CLI003"]
    })

    result = check_reference(
        bookings,
        "client_id",
        clients,
        "client_id"
    )

    assert result is True


def test_invalid_reference():
    bookings = pd.DataFrame({
        "client_id": ["CLI001", "CLI999"]
    })

    clients = pd.DataFrame({
        "client_id": ["CLI001", "CLI002"]
    })

    result = check_reference(
        bookings,
        "client_id",
        clients,
        "client_id"
    )

    assert result is False

def test_valid_date_order():
    df = pd.DataFrame({
        "booking_date": pd.to_datetime([
            "2026-01-10",
            "2026-02-01"
        ]),
        "event_date": pd.to_datetime([
            "2026-01-20",
            "2026-02-15"
        ])
    })

    result = check_date_order(
        df,
        "booking_date",
        "event_date"
    )

    assert result is True


def test_invalid_date_order():
    df = pd.DataFrame({
        "booking_date": pd.to_datetime([
            "2026-05-20"
        ]),
        "event_date": pd.to_datetime([
            "2026-05-10"
        ])
    })

    result = check_date_order(
        df,
        "booking_date",
        "event_date"
    )

    assert result is False


def test_valid_allowed_values():
    df = pd.DataFrame({
        "status": [
            "Pending",
            "Confirmed",
            "Completed"
        ]
    })

    result = check_allowed_values(
        df,
        "status",
        [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled"
        ]
    )

    assert result is True


def test_invalid_allowed_values():
    df = pd.DataFrame({
        "status": [
            "Pending",
            "Lunas Banget"
        ]
    })

    result = check_allowed_values(
        df,
        "status",
        [
            "Pending",
            "Confirmed",
            "Completed",
            "Cancelled"
        ]
    )

    assert result is False

def test_payment_after_booking_valid():
    bookings = pd.DataFrame({
        "booking_id": ["BOOK001", "BOOK002"],
        "booking_date": pd.to_datetime([
            "2026-01-10",
            "2026-02-01"
        ])
    })

    payments = pd.DataFrame({
        "booking_id": ["BOOK001", "BOOK002"],
        "payment_date": pd.to_datetime([
            "2026-01-10",
            "2026-02-05"
        ])
    })

    result = check_payment_after_booking(
        payments,
        bookings
    )

    assert result is True


def test_payment_after_booking_invalid():
    bookings = pd.DataFrame({
        "booking_id": ["BOOK001"],
        "booking_date": pd.to_datetime([
            "2026-03-10"
        ])
    })

    payments = pd.DataFrame({
        "booking_id": ["BOOK001"],
        "payment_date": pd.to_datetime([
            "2026-03-01"
        ])
    })

    result = check_payment_after_booking(
        payments,
        bookings
    )

    assert result is False


