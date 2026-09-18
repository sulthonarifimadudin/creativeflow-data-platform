import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = BASE_DIR / "data" / "raw"


def extract_clients():
    return pd.read_csv(RAW_DATA_DIR / "clients.csv")


def extract_packages():
    return pd.read_csv(RAW_DATA_DIR / "packages.csv")


def extract_photographers():
    return pd.read_csv(RAW_DATA_DIR / "photographers.csv")


def extract_bookings():
    return pd.read_csv(RAW_DATA_DIR / "bookings.csv")


def extract_payments():
    return pd.read_csv(RAW_DATA_DIR / "payments.csv")


if __name__ == "__main__":
    clients = extract_clients()
    packages = extract_packages()
    photographers = extract_photographers()
    bookings = extract_bookings()
    payments = extract_payments()

    print("=== EXTRACT SUMMARY ===")
    print(f"Clients       : {len(clients)} rows")
    print(f"Packages      : {len(packages)} rows")
    print(f"Photographers : {len(photographers)} rows")
    print(f"Bookings      : {len(bookings)} rows")
    print(f"Payments      : {len(payments)} rows")