import csv
import os
import random
import argparse
import pandas as pd
from datetime import datetime, timedelta

# --- Metadata ---
VERSION = "2026.1.0"
DATA_DIR = "data"
DATE_FILE = "current_date_time.txt"

# --- Path & File Helpers ---


def get_inventory_file_path(filename="inventory.csv"):
    """Returns path to files inside the data directory, ensuring directory exists."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    return os.path.join(DATA_DIR, filename)


# --- CSV Handling (Upgraded to Pandas for Logic, Dict for legacy) ---


def read_csv(filename="inventory.csv"):
    """
    Reads CSV using Pandas. This is the primary reader for business logic.
    Returns an empty DataFrame with expected columns if the file is missing or empty.
    """
    path = get_inventory_file_path(filename)
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        return pd.DataFrame(
            columns=[
                "product_name",
                "count",
                "buy_price",
                "expiration_date",
                "buy_date",
            ]
        )
    return pd.read_csv(path)


def write_csv(df, filename="inventory.csv"):
    """Writes a Pandas DataFrame to the data directory."""
    path = get_inventory_file_path(filename)
    df.to_csv(path, index=False)


def read_csv_dict_legacy(filepath):
    """Kept for backwards compatibility with legacy list-of-dict logic."""
    if not os.path.exists(filepath):
        return []
    with open(filepath, mode="r", newline="", encoding="utf-8") as file:
        return list(csv.DictReader(file))


# --- Record Creation & Data Gen ---


def create_buy_record(args):
    """Converts Argparse namespace into a dictionary for storage."""
    return {
        "product_name": args.product,
        "buy_price": args.buy_price,
        "count": args.quantity,
        "buy_date": args.buy_date.strftime("%Y-%m-%d"),
        "expiration_date": args.exp_date.strftime("%Y-%m-%d"),
    }


def random_dates(start_date, end_date, n=10):
    """Generates random dates between two points for mock data."""
    start_timestamp = datetime.timestamp(start_date)
    end_timestamp = datetime.timestamp(end_date)
    random_dates_list = []
    for _ in range(n):
        ts = random.randint(int(start_timestamp), int(end_timestamp))
        random_dates_list.append(datetime.fromtimestamp(ts))
    return random_dates_list


# --- Date Management (Simulation Clock) ---


def get_current_date_time():
    """Reads the 'simulated' date from the internal state file."""
    if not os.path.exists(DATE_FILE):
        with open(DATE_FILE, "w") as f:
            # Initialize with current system time if missing
            f.write(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))

    with open(DATE_FILE, "r") as f:
        return datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S.%f")


def advance_date_time(days=1):
    """Advances the simulated clock by N days and updates internal state."""
    current = get_current_date_time()
    new_date = current + timedelta(days=days)
    with open(DATE_FILE, "w") as f:
        f.write(new_date.strftime("%Y-%m-%d %H:%M:%S.%f"))
    return new_date


# --- CLI Argument Validation ---


def valid_date(s):
    """
    Validator for argparse.
    Returns a datetime object for consistency across the app.
    """
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = f"Not a valid date: '{s}'. Use YYYY-MM-DD."
        raise argparse.ArgumentTypeError(msg)
