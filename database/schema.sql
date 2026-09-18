CREATE TABLE dim_client (
    client_key BIGSERIAL PRIMARY KEY,
    client_id TEXT NOT NULL UNIQUE,
    name TEXT,
    email TEXT,
    phone TEXT,
    city TEXT,
    created_date TIMESTAMP
);

CREATE TABLE dim_package (
    package_key BIGSERIAL PRIMARY KEY,
    package_id TEXT NOT NULL UNIQUE,
    package_name TEXT,
    category TEXT,
    price BIGINT,
    duration_hour BIGINT
);

CREATE TABLE dim_photographer (
    photographer_key BIGSERIAL PRIMARY KEY,
    photographer_id TEXT NOT NULL UNIQUE,
    name TEXT,
    specialization TEXT,
    experience_year BIGINT
);

CREATE TABLE dim_date (
    date_key INTEGER PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    day INTEGER,
    month_name TEXT,
    day_name TEXT,
    quarter INTEGER
);

CREATE TABLE fact_booking (
    booking_key BIGSERIAL PRIMARY KEY,
    booking_id TEXT NOT NULL UNIQUE,
    client_key BIGINT NOT NULL,
    package_key BIGINT NOT NULL,
    photographer_key BIGINT NOT NULL,
    booking_date DATE,
    event_date DATE,
    status TEXT,

    FOREIGN KEY (client_key)
        REFERENCES dim_client(client_key),

    FOREIGN KEY (package_key)
        REFERENCES dim_package(package_key),

    FOREIGN KEY (photographer_key)
        REFERENCES dim_photographer(photographer_key)
);

CREATE TABLE fact_payment (
    payment_key BIGSERIAL PRIMARY KEY,
    payment_id TEXT NOT NULL UNIQUE,
    booking_key BIGINT NOT NULL,
    payment_date DATE,
    amount BIGINT,
    payment_method TEXT,
    status TEXT,

    FOREIGN KEY (booking_key)
        REFERENCES fact_booking(booking_key)
);