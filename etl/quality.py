def check_duplicates(df, column):
    return bool(not df[column].duplicated().any())


def check_required_columns(df, columns):
    return bool(not df[columns].isnull().any().any())


def check_positive_values(df, column):
    return bool((df[column] > 0).all())

def check_date_order(df, start_column, end_column):
    return bool(
        (df[end_column] >= df[start_column]).all()
    )


def check_allowed_values(df, column, allowed_values):
    return bool(
        df[column].isin(allowed_values).all()
    )

def validate_clients(clients):
    return {
        "client_id_not_duplicate": check_duplicates(
            clients,
            "client_id"
        ),
        "client_required_columns": check_required_columns(
            clients,
            ["client_id", "name", "email"]
        )
    }


def validate_packages(packages):
    return {
        "package_id_not_duplicate": check_duplicates(
            packages,
            "package_id"
        ),
        "package_required_columns": check_required_columns(
            packages,
            ["package_id", "package_name", "price"]
        ),
        "package_price_positive": check_positive_values(
            packages,
            "price"
        )
    }


def validate_photographers(photographers):
    return {
        "photographer_id_not_duplicate": check_duplicates(
            photographers,
            "photographer_id"
        ),
        "photographer_required_columns": check_required_columns(
            photographers,
            ["photographer_id", "name"]
        )
    }


def validate_bookings(
    bookings,
    clients,
    packages,
    photographers
):
    return {
        "booking_id_not_duplicate":
            check_duplicates(
                bookings,
                "booking_id"
            ),

        "booking_required_columns":
            check_required_columns(
                bookings,
                [
                    "booking_id",
                    "client_id",
                    "package_id",
                    "photographer_id",
                    "booking_date",
                    "event_date"
                ]
            ),

        "booking_client_reference":
            check_reference(
                bookings,
                "client_id",
                clients,
                "client_id"
            ),

        "booking_package_reference":
            check_reference(
                bookings,
                "package_id",
                packages,
                "package_id"
            ),

        "booking_photographer_reference":
            check_reference(
                bookings,
                "photographer_id",
                photographers,
                "photographer_id"
            ),
        "booking_date_order":
            check_date_order(
                bookings,
                "booking_date",
                "event_date"
            ),

        "booking_status_valid":
            check_allowed_values(
                bookings,
                "status",
            [
                "Pending",
                "Confirmed",
                "Completed",
                "Cancelled"
            ]
        )
    }


def validate_payments(
    payments,
    bookings
):
    return {
        "payment_id_not_duplicate":
            check_duplicates(
                payments,
                "payment_id"
            ),

        "payment_required_columns":
            check_required_columns(
                payments,
                [
                    "payment_id",
                    "booking_id",
                    "payment_date",
                    "amount"
                ]
            ),

        "payment_amount_positive":
            check_positive_values(
                payments,
                "amount"
            ),

        "payment_booking_reference":
            check_reference(
                payments,
                "booking_id",
                bookings,
                "booking_id"
            ),

        "payment_status_valid":
            check_allowed_values(
                payments,
                "status",
                [
                    "Paid",
                    "Pending",
                    "Failed"
                ]
            ),
            
        "payment_after_booking":
            check_payment_after_booking(
                payments,
                bookings
        )
    }

def print_quality_report(dataset_name, checks):
    print()
    print(f"=== DATA QUALITY: {dataset_name.upper()} ===")

    all_passed = True

    for check_name, passed in checks.items():
        status = "PASS" if passed else "FAIL"
        print(f"{status} - {check_name}")

        if not passed:
            all_passed = False

    return all_passed

def check_reference(child_df, child_column, parent_df, parent_column):
    valid_values = set(parent_df[parent_column])

    return bool(
        child_df[child_column]
        .isin(valid_values)
        .all()
    )

def check_payment_after_booking(payments, bookings):
    booking_dates = bookings[
        ["booking_id", "booking_date"]
    ]

    merged = payments.merge(
        booking_dates,
        on="booking_id",
        how="left"
    )

    return bool(
        (
            merged["payment_date"]
            >= merged["booking_date"]
        ).all()
    )

if __name__ == "__main__":
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

    clients = transform_clients(extract_clients())
    packages = transform_packages(extract_packages())
    photographers = transform_photographers(
        extract_photographers()
    )
    bookings = transform_bookings(extract_bookings())
    payments = transform_payments(extract_payments())

    results = [
    print_quality_report(
        "clients",
        validate_clients(clients)
    ),

    print_quality_report(
        "packages",
        validate_packages(packages)
    ),

    print_quality_report(
        "photographers",
        validate_photographers(photographers)
    ),

    print_quality_report(
        "bookings",
        validate_bookings(
            bookings,
            clients,
            packages,
            photographers
        )
    ),

    print_quality_report(
        "payments",
        validate_payments(
            payments,
            bookings
        )
    )
]
    print()
    print("==============================")

    if all(results):
        print("OVERALL DATA QUALITY: PASS")
    else:
        print("OVERALL DATA QUALITY: FAIL")