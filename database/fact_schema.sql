CREATE TABLE dim_date (
    date_key SERIAL PRIMARY KEY,
    full_date DATE NOT NULL,
    year INTEGER,
    month INTEGER,
    month_name VARCHAR(20),
    quarter INTEGER
);


CREATE TABLE fact_booking (
    booking_key SERIAL PRIMARY KEY,

    booking_id VARCHAR(20) NOT NULL,

    client_key INTEGER REFERENCES dim_client(client_key),
    package_key INTEGER REFERENCES dim_package(package_key),
    photographer_key INTEGER REFERENCES dim_photographer(photographer_key),

    booking_date DATE,
    event_date DATE,

    status VARCHAR(50)
);


CREATE TABLE fact_payment (
    payment_key SERIAL PRIMARY KEY,

    payment_id VARCHAR(20) NOT NULL,

    booking_id VARCHAR(20),

    payment_date DATE,

    amount INTEGER,

    payment_method VARCHAR(50),

    status VARCHAR(50)
);