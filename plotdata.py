import matplotlib.pyplot as plt
import pandas as pd
import os

# Configuration: Path to your data folder
DATA_DIR = "data"


def load_csv(filename):
    """Safely loads a CSV from the data directory."""
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"Warning: {path} not found.")
        return pd.DataFrame()
    return pd.read_csv(path)


def plot_combined_report():
    """
    Loads data and creates a comprehensive visual report.
    Adjusted for typical SuperPy column names.
    """
    bought = load_csv("bought.csv")
    sold = load_csv("sold.csv")

    if bought.empty or sold.empty:
        print("Not enough data to generate plots.")
        return

    # SuperPy logic: We often need to aggregate counts per date
    # Adjust 'buy_date' or 'sell_date' based on your actual CSV headers
    bought_counts = bought.groupby("buy_date").size()
    sold_counts = sold.groupby("sell_date").size()

    plt.figure(figsize=(12, 6))

    plt.plot(
        bought_counts.index,
        bought_counts.values,
        label="Items Bought",
        marker="o",
        linestyle="-",
    )
    plt.plot(
        sold_counts.index,
        sold_counts.values,
        label="Items Sold",
        marker="s",
        linestyle="--",
    )

    plt.title("Business Activity Over Time", fontsize=14)
    plt.xlabel("Date")
    plt.ylabel("Number of Items")
    plt.xticks(rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.grid(True, alpha=0.3)

    plt.show()


def plot_revenue_vs_cost():
    """
    Advanced: Compare buy_price vs sell_price over time.
    """
    # This assumes your CSVs have 'buy_price' and 'sell_price'
    bought = load_csv("bought.csv")
    sold = load_csv("sold.csv")

    if "buy_price" in bought.columns and "sell_price" in sold.columns:
        total_cost = bought.groupby("buy_date")["buy_price"].sum()
        total_rev = sold.groupby("sell_date")["sell_price"].sum()

        plt.figure(figsize=(10, 5))
        total_cost.plot(kind="bar", color="red", alpha=0.5, label="Expenses")
        total_rev.plot(kind="bar", color="green", alpha=0.5, label="Revenue")
        plt.title("Financial Overview")
        plt.legend()
        plt.show()


if __name__ == "__main__":
    # This allows you to run this file independently for testing
    plot_combined_report()
