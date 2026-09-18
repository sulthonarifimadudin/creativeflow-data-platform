import pandas as pd

from database import engine
from sqlalchemy import text

from extract import (
    extract_clients,
    extract_packages,
    extract_photographers,
    extract_bookings,
    extract_payments
)

from transform import (
    transform_clients,
    transform_packages,
    transform_photographers,
    transform_bookings,
    transform_payments
)


def load_clients():
    clients = extract_clients()
    transformed_clients = transform_clients(clients)

    upsert_dataframe(
        transformed_clients,
        table_name="dim_client",
        conflict_column="client_id",
        update_columns=[
            "name",
            "email",
            "phone",
            "city",
            "created_date"
        ]
    )

    print(
        f"Loaded {len(transformed_clients)} clients "
        "into dim_client"
    )


def load_packages():
    packages = extract_packages()
    transformed_packages = transform_packages(packages)

    upsert_dataframe(
        transformed_packages,
        table_name="dim_package",
        conflict_column="package_id",
        update_columns=[
            "package_name",
            "category",
            "price",
            "duration_hour"
        ]
    )

    print(
        f"Loaded {len(transformed_packages)} packages "
        "into dim_package"
    )


def load_photographers():
    photographers = extract_photographers()
    transformed_photographers = transform_photographers(
        photographers
    )

    upsert_dataframe(
        transformed_photographers,
        table_name="dim_photographer",
        conflict_column="photographer_id",
        update_columns=[
            "name",
            "specialization",
            "experience_year"
        ]
    )

    print(
        f"Loaded {len(transformed_photographers)} photographers "
        "into dim_photographer"
    )



def load_payments():
    # Extract
    payments = extract_payments()

    # Transform
    transformed_payments = transform_payments(payments)

    # Ambil booking key dari database
    bookings = pd.read_sql(
        """
        SELECT booking_key, booking_id
        FROM fact_booking
        """,
        engine
    )

    # Lookup booking_key
    transformed_payments = transformed_payments.merge(
        bookings,
        on="booking_id",
        how="left"
    )

    # Pilih kolom yang dibutuhkan fact table
    transformed_payments = transformed_payments[
        [
            "payment_id",
            "booking_key",
            "payment_date",
            "amount",
            "payment_method",
            "status"
        ]
    ]

    # Load
    upsert_dataframe(
        transformed_payments,
        table_name="fact_payment",
        conflict_column="payment_id",
        update_columns=[
            "booking_key",
            "payment_date",
            "amount",
            "payment_method",
            "status"
        ]
    )

    print(
        f"Loaded {len(transformed_payments)} payments "
        "into fact_payment"
    )

    print("=== FACT PAYMENT ===")
    print(transformed_payments)
    
def load_bookings():
    # Extract
    bookings = extract_bookings()

    # Transform
    transformed_bookings = transform_bookings(bookings)

    # Ambil dimension dari database
    clients = pd.read_sql(
        "SELECT client_key, client_id FROM dim_client",
        engine
    )

    packages = pd.read_sql(
        "SELECT package_key, package_id FROM dim_package",
        engine
    )

    photographers = pd.read_sql(
        """
        SELECT photographer_key, photographer_id
        FROM dim_photographer
        """,
        engine
    )

    # Lookup client_key
    transformed_bookings = transformed_bookings.merge(
        clients,
        on="client_id",
        how="left"
    )

    # Lookup package_key
    transformed_bookings = transformed_bookings.merge(
        packages,
        on="package_id",
        how="left"
    )

    # Lookup photographer_key
    transformed_bookings = transformed_bookings.merge(
        photographers,
        on="photographer_id",
        how="left"
    )

    # Pilih kolom yang dibutuhkan fact table
    transformed_bookings = transformed_bookings[
        [
            "booking_id",
            "client_key",
            "package_key",
            "photographer_key",
            "booking_date",
            "event_date",
            "status"
        ]
    ]

    upsert_dataframe(
        transformed_bookings,
        table_name="fact_booking",
        conflict_column="booking_id",
        update_columns=[
            "client_key",
            "package_key",
            "photographer_key",
            "booking_date",
            "event_date",
            "status"
        ]
)

    print(
        f"Loaded {len(transformed_bookings)} bookings "
        "into fact_booking"
    )

    print("=== AFTER KEY LOOKUP ===")
    print(transformed_bookings)

def upsert_dataframe(
    df,
    table_name,
    conflict_column,
    update_columns
):
    if df.empty:
        print(f"No data to load into {table_name}")
        return

    columns = list(df.columns)

    column_names = ", ".join(columns)

    value_names = ", ".join(
        [f":{column}" for column in columns]
    )

    update_statement = ", ".join(
        [
            f"{column} = EXCLUDED.{column}"
            for column in update_columns
        ]
    )

    query = text(
        f"""
        INSERT INTO {table_name}
        ({column_names})
        VALUES ({value_names})

        ON CONFLICT ({conflict_column})
        DO UPDATE SET
        {update_statement}
        """
    )

    records = df.to_dict(
        orient="records"
    )

    with engine.begin() as connection:
        connection.execute(
            query,
            records
        )

    print(
        f"{len(df)} rows upserted into {table_name}"
    )

if __name__ == "__main__":
    load_clients()
    load_packages()
    load_photographers()

    load_bookings()
    load_payments()