import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
from datetime import datetime


def plot_inventory_over_time(inventory_data):
    """
    Plots inventory data over time.

    Parameters:
    inventory_data (DataFrame): A DataFrame containing 'date' and 'count' columns.

    Returns:
    None
    """
    if "date" not in inventory_data.columns or "count" not in inventory_data.columns:
        raise ValueError("Columns 'date' or 'count' not found in DataFrame")

    # Convert 'date' column to datetime
    inventory_data["date"] = pd.to_datetime(inventory_data["date"])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(inventory_data["date"], inventory_data["count"], marker="o")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title("Inventory Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.show()


def plot_bought_over_time(bought_data):
    """
    Plots bought data over time.

    Parameters:
    bought_data (DataFrame): A DataFrame containing 'date' and 'count' columns.

    Returns:
    None
    """
    if "date" not in bought_data.columns or "count" not in bought_data.columns:
        raise ValueError("Columns 'date' or 'count' not found in DataFrame")

    # Convert 'date' column to datetime
    bought_data["date"] = pd.to_datetime(bought_data["date"])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(bought_data["date"], bought_data["count"], marker="o")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title("Bought Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.show()


def plot_data_over_time(data, title):
    """
    Plots data over time.

    Parameters:
    data (DataFrame): A DataFrame containing 'date' and 'count' columns.
    title (str): The title of the plot.

    Returns:
    None
    """
    if "date" not in data.columns or "count" not in data.columns:
        raise ValueError("Columns 'date' or 'count' not found in DataFrame")

    # Convert 'date' column to datetime
    data["date"] = pd.to_datetime(data["date"])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(data["date"], data["count"], marker="o")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.show()


def plot_expired_over_time(expired_data):
    """
    Plots expired data over time.

    Parameters:
    expired_data (DataFrame): A DataFrame containing 'date' and 'count' columns.

    Returns:
    None
    """
    if "date" not in expired_data.columns or "count" not in expired_data.columns:
        raise ValueError("Columns 'date' or 'count' not found in DataFrame")

    # Convert 'date' column to datetime
    expired_data["date"] = pd.to_datetime(expired_data["date"])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(expired_data["date"], expired_data["count"], marker="o")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title("Expired Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.show()


def plot_multiple_data_over_time(data_dict):
    """
    Plots multiple data over time.

    Parameters:
    data_dict (dict): A dictionary where keys are titles and values are DataFrames containing 'date' and 'count' columns.

    Returns:
    None
    """
    plt.figure(figsize=(10, 6))
    for title, data in data_dict.items():
        if "date" not in data.columns or "count" not in data.columns:
            raise ValueError(
                f"Columns 'date' or 'count' not found in DataFrame for {title}"
            )

        data["date"] = pd.to_datetime(data["date"])
        plt.plot(data["date"], data["count"], marker="o", label=title)

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title("Data Over Time")
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.legend()
    plt.show()


# Load the CSV data into Pandas DataFrames
bought_data = pd.read_csv("data/bought.csv")
sold_data = pd.read_csv("data/sold.csv")
inventory_data = pd.read_csv("data/inventory.csv")

# Add 'date' and 'count' columns to the DataFrames
date = datetime.now().strftime("%Y-%m-%d")
count = 1
data_list = [
    (bought_data, "bought_data"),
    (sold_data, "sold_data"),
    (inventory_data, "inventory_data"),
]
for data, name in data_list:
    data["date"] = date
    data["count"] = count

# Check if 'date' and 'count' columns are present in the data
for data, name in data_list:
    if "date" not in data.columns or "count" not in data.columns:
        print(f"'date' or 'count' column not found in {name}")
    else:
        print(f"'date' and 'count' columns found in {name}")

# Plot the data
plot_data_over_time(inventory_data, "Inventory Over Time")
plot_data_over_time(bought_data, "Bought Over Time")
plot_data_over_time(sold_data, "Sold Over Time")

data_dict = {"Inventory": inventory_data, "Bought": bought_data, "Sold": sold_data}
plot_multiple_data_over_time(data_dict)


def plot_sold_over_time(sold_data):
    """
    Plots sold data over time.

    Parameters:
    sold_data (DataFrame): A DataFrame containing 'date' and 'amount' columns.

    Returns:
    None
    """
    if "date" not in sold_data.columns or "amount" not in sold_data.columns:
        raise ValueError("Columns 'date' or 'amount' not found in DataFrame")

    # Convert 'date' column to datetime
    sold_data["date"] = pd.to_datetime(sold_data["date"])

    # Plot the data
    plt.figure(figsize=(10, 6))
    plt.plot(sold_data["date"], sold_data["amount"], marker="o")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title("Sold Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.show()


def plot_sales_over_time(sales_data):
    dates = [datetime.strptime(date, "%Y-%m-%d") for date, amount in sales_data]
    amounts = [amount for date, amount in sales_data]

    plt.figure(figsize=(10, 6))
    plt.plot(dates, amounts, marker="o")
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.gcf().autofmt_xdate()
    plt.title("Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.show()


print(inventory_data.columns)
print(bought_data.columns)
print(sold_data.columns)
