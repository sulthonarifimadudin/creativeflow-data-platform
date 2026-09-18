import pandas as pd



def transform_clients(clients):
    df = clients.copy()

    # Phone number harus diperlakukan sebagai string
    df["phone"] = df["phone"].astype(str)

    # Tambahkan leading zero jika belum ada
    df["phone"] = df["phone"].apply(
        lambda phone: phone if phone.startswith("0") else "0" + phone
    )

    # Pastikan created_date menjadi datetime
    df["created_date"] = pd.to_datetime(
        df["created_date"],
        errors="coerce"
    )

    # Hapus duplicate berdasarkan client_id
    df = df.drop_duplicates(
        subset=["client_id"]
    )

    return df


def transform_packages(packages):
    df = packages.copy()

    # Pastikan price berupa numeric
    df["price"] = pd.to_numeric(
        df["price"],
        errors="coerce"
    )

    # Pastikan duration berupa integer
    df["duration_hour"] = pd.to_numeric(
        df["duration_hour"],
        errors="coerce"
    )

    # Hapus duplicate package
    df = df.drop_duplicates(
        subset=["package_id"]
    )

    return df

def transform_photographers(photographers):
    df = photographers.copy()

    # Pastikan experience_year berupa numeric
    df["experience_year"] = pd.to_numeric(
        df["experience_year"],
        errors="coerce"
    )

    # Hapus duplicate photographer
    df = df.drop_duplicates(
        subset=["photographer_id"]
    )

    return df

def transform_bookings(bookings):
    df = bookings.copy()

    # Pastikan tanggal menjadi datetime
    df["booking_date"] = pd.to_datetime(
        df["booking_date"],
        errors="coerce"
    )

    df["event_date"] = pd.to_datetime(
        df["event_date"],
        errors="coerce"
    )

    # Hapus duplicate booking
    df = df.drop_duplicates(
        subset=["booking_id"]
    )

    return df

def transform_payments(payments):
    df = payments.copy()

    # Pastikan tanggal menjadi datetime
    df["payment_date"] = pd.to_datetime(
        df["payment_date"],
        errors="coerce"
    )

    # Pastikan amount berupa numeric
    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce"
    )

    # Hapus duplicate payment
    df = df.drop_duplicates(
        subset=["payment_id"]
    )

    return df


if __name__ == "__main__":
    from extract import (
        extract_clients,
        extract_packages,
        extract_photographers,
        extract_bookings,
        extract_payments
    )

    # Extract
    clients = extract_clients()
    packages = extract_packages()
    photographers = extract_photographers()
    bookings = extract_bookings()
    payments = extract_payments()
    
    # Transform
    transformed_clients = transform_clients(clients)
    transformed_packages = transform_packages(packages)
    transformed_photographers = transform_photographers(photographers)
    transformed_bookings = transform_bookings(bookings)
    transformed_payments = transform_payments(payments)

    # Output
    print("=== CLIENTS ===")
    print(transformed_clients)

    print()
    print("=== CLIENT DATA TYPES ===")
    print(transformed_clients.dtypes)

    print()
    print("=== PACKAGES ===")
    print(transformed_packages)

    print()
    print("=== PACKAGE DATA TYPES ===")
    print(transformed_packages.dtypes)

    print()
    print("=== PHOTOGRAPHERS ===")
    print(transformed_photographers)

    print()
    print("=== PHOTOGRAPHER DATA TYPES ===")
    print(transformed_photographers.dtypes)

    print()
    print("=== BOOKINGS ===")
    print(transformed_bookings)

    print()
    print("=== BOOKING DATA TYPES ===")
    print(transformed_bookings.dtypes)

    print()
    print("=== PAYMENTS ===")
    print(transformed_payments)

    print()
    print("=== PAYMENT DATA TYPES ===")
    print(transformed_payments.dtypes)