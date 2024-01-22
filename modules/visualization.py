import matplotlib.pyplot as plt  # for plotting
import matplotlib.dates as mdates  # for formatting dates on x-axis
import matplotlib.ticker as mticker  # for formatting y-axis
from datetime import datetime  # for parsing dates


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

