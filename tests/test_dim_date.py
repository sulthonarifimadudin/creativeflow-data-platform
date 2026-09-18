import pandas as pd

from etl.dim_date import (
    generate_dim_date,
    get_date_range
)


def test_generate_dim_date():
    df = generate_dim_date(
        start_date="2026-01-01",
        end_date="2026-01-03"
    )

    assert len(df) == 3

    assert df.iloc[0]["date_key"] == 20260101
    assert df.iloc[0]["year"] == 2026
    assert df.iloc[0]["month"] == 1
    assert df.iloc[0]["day"] == 1
    assert df.iloc[0]["quarter"] == 1


def test_dim_date_has_no_duplicate_date_key():
    df = generate_dim_date(
        start_date="2026-01-01",
        end_date="2026-01-10"
    )

    assert df["date_key"].duplicated().any() == False

def test_get_date_range():
    bookings = pd.DataFrame({
        "booking_date": pd.to_datetime([
            "2026-01-15",
            "2026-03-10"
        ]),
        "event_date": pd.to_datetime([
            "2026-03-20",
            "2026-05-20"
        ])
    })

    payments = pd.DataFrame({
        "payment_date": pd.to_datetime([
            "2026-01-15",
            "2026-03-18"
        ])
    })

    start_date, end_date = get_date_range(
        bookings,
        payments
    )

    assert start_date == pd.Timestamp("2026-01-15")
    assert end_date == pd.Timestamp("2026-05-20")