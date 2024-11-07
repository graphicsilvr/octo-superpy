import csv
import os
import random
from datetime import datetime, timedelta


def get_inventory_file_path(filename):
    return os.path.join("data", filename)


def read_csv(filepath):
    with open(filepath, mode="r", newline="") as file:
        return list(csv.DictReader(file))


def write_csv(filepath, data):
    with open(filepath, mode="w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def create_buy_record(args):
    return {
        "product": args.product,
        "buy-price": args.buy_price,
        "quantity": args.quantity,
        "buy-date": args.buy_date.strftime("%Y-%m-%d"),
        "exp-date": args.exp_date.strftime("%Y-%m-%d"),
    }


def random_dates(start_date, end_date, n=10):
    start_timestamp = datetime.timestamp(start_date)
    end_timestamp = datetime.timestamp(end_date)
    random_timestamps = [
        random.randint(start_timestamp, end_timestamp) for _ in range(n)
    ]
    random_dates = [
        datetime.fromtimestamp(timestamp) for timestamp in random_timestamps
    ]
    return random_dates


def read_bought_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def write_bought_csv(filename, data):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


def read_sold_csv(filename):
    with open(filename, "r") as f:
        reader = csv.reader(f)
        data = list(reader)
    return data


def write_sold_csv(filename, data):
    with open(filename, "w") as f:
        writer = csv.writer(f)
        writer.writerows(data)


# Create a file 'current_date_time.txt' to store the current date and time
with open("current_date_time.txt", "w") as f:
    f.write(str(datetime.now()))


def advance_date_time():
    with open("current_date_time.txt", "r") as f:
        current_date_time = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S.%f")
    with open("current_date_time.txt", "w") as f:
        f.write(str(current_date_time + timedelta(days=1)))


def get_current_date_time():
    with open("current_date_time.txt", "r") as f:
        current_date_time = datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S.%f")
    return current_date_time
