"""Download a HM Land Registry Price Paid yearly file and load it,
unchanged, into the raw layer of Postgres.

Usage: python ingest/load_price_paid.py 2025
"""
import os
import sys
import urllib.request
from pathlib import Path

import psycopg
from dotenv import load_dotenv

BASE_URL = "https://price-paid-data.publicdata.landregistry.gov.uk"
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"

# The source files have no header row, so the column names are defined here.
COLUMNS = [
    "transaction_id", "price", "date_of_transfer", "postcode",
    "property_type", "old_new", "duration", "paon", "saon", "street",
    "locality", "town_city", "district", "county",
    "ppd_category_type", "record_status",
]
COL_LIST = ", ".join(COLUMNS)
COL_DEFS = ", ".join(f"{c} text" for c in COLUMNS)


def download(year: str) -> Path:
    DATA_DIR.mkdir(exist_ok=True)
    filename = f"pp-{year}.csv"
    path = DATA_DIR / filename
    if path.exists():
        print(f"{filename} already downloaded, skipping")
    else:
        print(f"Downloading {filename} ...")
        urllib.request.urlretrieve(f"{BASE_URL}/{filename}", path)
    return path


def load(path: Path) -> None:
    load_dotenv(PROJECT_ROOT / ".env")
    conn = psycopg.connect(
        host=os.environ.get("POSTGRES_HOST", "localhost"),
        port=5432,
        dbname=os.environ["POSTGRES_DB"],
        user=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
    )
    with conn, conn.cursor() as cur:
        cur.execute("CREATE SCHEMA IF NOT EXISTS raw")
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS raw.price_paid (
                    {COL_DEFS},
                    source_file text,
                    loaded_at timestamptz DEFAULT now())"""
        )
        # Load into a temp table first, so re-running the script never duplicates rows
        cur.execute(f"CREATE TEMP TABLE staging ({COL_DEFS}) ON COMMIT DROP")
        with open(path, "rb") as f, cur.copy(
            f"COPY staging ({COL_LIST}) FROM STDIN WITH (FORMAT csv)"
        ) as copy:
            while chunk := f.read(1 << 20):
                copy.write(chunk)

        cur.execute("DELETE FROM raw.price_paid WHERE source_file = %s", (path.name,))
        cur.execute(
            f"""INSERT INTO raw.price_paid ({COL_LIST}, source_file)
                SELECT {COL_LIST}, %s FROM staging""",
            (path.name,),
        )
        cur.execute(
            "SELECT count(*) FROM raw.price_paid WHERE source_file = %s",
            (path.name,),
        )
        print(f"Loaded {cur.fetchone()[0]:,} rows from {path.name}")


if __name__ == "__main__":
    year = sys.argv[1] if len(sys.argv) > 1 else "2025"
    load(download(year))
