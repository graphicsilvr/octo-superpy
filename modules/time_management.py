from datetime import datetime, timedelta


def advance_time(args):
    date_file = "current_date.txt"
    try:
        # Try to read the current date from the file
        with open(date_file, "r") as file:
            current_date_str = file.read().strip()
            current_date = datetime.strptime(current_date_str, "%Y-%m-%d")
    except FileNotFoundError:
        # If the file doesn't exist, assume today's date
        current_date = datetime.today()
    except ValueError:
        # If the date in the file is invalid, also assume today's date
        print("Invalid date found in file, using today's date instead.")
        current_date = datetime.today()

    # Advance the date
    new_date = current_date + timedelta(days=args.days)

    # Save the new date back to the file
    with open(date_file, "w") as file:
        file.write(new_date.strftime("%Y-%m-%d"))

    print(
        f"Time advanced by {args.days} days. New date is {new_date.strftime('%Y-%m-%d')}."
    )


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
