CREATE SCHEMA IF NOT EXISTS raw;

CREATE TABLE IF NOT EXISTS raw.price_paid (
    transaction_id text, price text, date_of_transfer text, postcode text,
    property_type text, old_new text, duration text, paon text, saon text,
    street text, locality text, town_city text, district text, county text,
    ppd_category_type text, record_status text,
    source_file text, loaded_at timestamptz DEFAULT now()
);

INSERT INTO raw.price_paid
    (transaction_id, price, date_of_transfer, postcode, property_type, old_new,
     duration, paon, saon, street, locality, town_city, district, county,
     ppd_category_type, record_status, source_file)
VALUES
 ('{00000000-0000-0000-0000-000000000001}', '250000', '2025-01-15 00:00', 'LS1 1AA', 'D', 'N', 'F', '1', '', 'TEST ROAD', '', 'Leeds', 'Leeds', 'West Yorkshire', 'A', 'A', 'ci_fixture'),
 ('{00000000-0000-0000-0000-000000000002}', '180000', '2025-01-20 00:00', 'LS2 2BB', 'T', 'N', 'F', '2', '', 'TEST STREET', '', 'Leeds', 'Leeds', 'West Yorkshire', 'A', 'A', 'ci_fixture'),
 ('{00000000-0000-0000-0000-000000000003}', '120000', '2025-02-03 00:00', 'M1 3CC', 'F', 'N', 'L', '3', 'FLAT 1', 'TEST LANE', '', 'Manchester', 'Manchester', 'Greater Manchester', 'A', 'A', 'ci_fixture'),
 ('{00000000-0000-0000-0000-000000000004}', '210000', '2025-02-10 00:00', 'M2 4DD', 'S', 'Y', 'F', '4', '', 'TEST CLOSE', '', 'Manchester', 'Manchester', 'Greater Manchester', 'A', 'A', 'ci_fixture'),
 ('{00000000-0000-0000-0000-000000000005}', '95000', '2025-02-12 00:00', 'M3 5EE', 'O', 'N', 'L', '5', '', 'TEST WAY', '', 'Manchester', 'Manchester', 'Greater Manchester', 'B', 'A', 'ci_fixture');
