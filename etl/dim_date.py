import pandas as pd

from database import engine
from extract import extract_bookings, extract_payments
from transform import transform_bookings, transform_payments
from sqlalchemy import text

def generate_dim_date(start_date, end_date):
    dates = pd.date_range(
        start=start_date,
        end=end_date,
        freq="D"
    )

    df = pd.DataFrame({
        "full_date": dates
    })

    df["date_key"] = (
        df["full_date"]
        .dt.strftime("%Y%m%d")
        .astype(int)
    )

    df["year"] = df["full_date"].dt.year
    df["month"] = df["full_date"].dt.month
    df["day"] = df["full_date"].dt.day

    df["month_name"] = (
        df["full_date"]
        .dt.month_name()
    )

    df["day_name"] = (
        df["full_date"]
        .dt.day_name()
    )

    df["quarter"] = (
        df["full_date"]
        .dt.quarter
    )

    return df[
        [
            "date_key",
            "full_date",
            "year",
            "month",
            "day",
            "month_name",
            "day_name",
            "quarter"
        ]
    ]

def get_date_range(bookings, payments):
    date_series = pd.concat(
        [
            bookings["booking_date"],
            bookings["event_date"],
            payments["payment_date"]
        ],
        ignore_index=True
    )

    start_date = date_series.min()
    end_date = date_series.max()

    return start_date, end_date

def upsert_dim_date(df):
    query = text("""
        INSERT INTO dim_date (
            date_key,
            full_date,
            year,
            month,
            day,
            month_name,
            day_name,
            quarter
        )
        VALUES (
            :date_key,
            :full_date,
            :year,
            :month,
            :day,
            :month_name,
            :day_name,
            :quarter
        )
        ON CONFLICT (date_key)
        DO UPDATE SET
            full_date = EXCLUDED.full_date,
            year = EXCLUDED.year,
            month = EXCLUDED.month,
            day = EXCLUDED.day,
            month_name = EXCLUDED.month_name,
            day_name = EXCLUDED.day_name,
            quarter = EXCLUDED.quarter
    """)

    records = df.to_dict(orient="records")

    with engine.begin() as connection:
        connection.execute(query, records)

    print(f"{len(df)} rows upserted into dim_date")

def load_dim_date():
    bookings = transform_bookings(
        extract_bookings()
    )

    payments = transform_payments(
        extract_payments()
    )

    start_date, end_date = get_date_range(
        bookings,
        payments
    )

    dim_date = generate_dim_date(
        start_date,
        end_date
    )

    upsert_dim_date(dim_date)

    print("=== DIM DATE RANGE ===")
    print(f"Start date : {start_date.date()}")
    print(f"End date   : {end_date.date()}")
    print(f"Total rows : {len(dim_date)}")

if __name__ == "__main__":
    load_dim_date()