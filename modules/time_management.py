from datetime import datetime, timedelta


def advance_time(days, file_path="data/current_date.txt"):
    with open(file_path, "r") as file:
        current_date = datetime.strptime(file.read().strip(), "%Y-%m-%d")
    new_date = current_date + timedelta(days=days)
    with open(file_path, "w") as file:
        file.write(new_date.strftime("%Y-%m-%d"))


def get_current_date(file_path):
    try:
        with open(file_path, "r") as file:
            return datetime.strptime(file.read().strip(), "%Y-%m-%d")
    except FileNotFoundError:
        return datetime.now()


def initialize_current_date(
    file_path="data/current_date.txt", default_date="2023-03-15"
):
    try:
        with open(file_path, "r") as file:
            # File exists, do nothing
            pass
    except FileNotFoundError:
        with open(file_path, "w") as file:
            # Write a default start date
            file.write(default_date)
