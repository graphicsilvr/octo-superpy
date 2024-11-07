import pandas as pd
import numpy as np
import argparse
from datetime import datetime, timedelta

# Set a seed for reproducibility
np.random.seed(42)


# Helper function to generate random dates
def random_dates(start, end, n=10):
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit="s")


now = pd.Timestamp("now")


def generate_inventory_data(num_products=100):
    now = pd.to_datetime("today")
    product_categories = ["Electronics", "Clothing", "Grocery", "Home"]
    inventory = []

    for _ in range(num_products):
        category = np.random.choice(product_categories)
        product_id = np.random.randint(1, 999)
        product_name = f"Product_{product_id}"
        quantity = np.random.randint(1, 100)
        price = np.random.uniform(10, 500).round(2)
        expiry_date = random_dates(now, now + timedelta(days=365 * 2))
        inventory.append(
            [product_id, product_name, quantity, price, category, expiry_date]
        )

    return inventory


def generate_expired_data(num_products=100):
    now = pd.to_datetime("today")
    expired = []

    for _ in range(num_products):
        product_id = np.random.randint(1, 999)
        product_name = f"Product_{product_id}"
        quantity = np.random.randint(1, 100)
        expiry_date = random_dates(
            now - timedelta(days=365 * 5), now - timedelta(days=365)
        )
        expired.append([product_id, product_name, quantity, expiry_date])

    return expired


def generate_revenue_data(num_products=100):
    inventory_df = pd.DataFrame(
        generate_inventory_data(num_products),
        columns=[
            "ProductID",
            "ProductName",
            "Quantity",
            "Price",
            "Category",
            "ExpiryDate",
        ],
    )
    revenue = (inventory_df["Price"] * inventory_df["Quantity"]).round(2)
    revenue_df = pd.DataFrame(
        {"ProductID": np.arange(1, num_products + 1), "Revenue": revenue}
    )
    return revenue_df


def generate_profit_data(num_products=100):
    revenue_df = generate_revenue_data(num_products)
    margin = 0.2
    profit = (revenue_df["Revenue"] * margin).round(2)
    profit_df = pd.DataFrame(
        {"ProductID": np.arange(1, num_products + 1), "Profit": profit}
    )
    return profit_df


def generate_bought_data(num_products=100):
    now = pd.to_datetime("today")
    bought = []

    for _ in range(num_products):
        product_id = np.random.randint(1, 999)
        product_name = f"Product_{product_id}"
        supplier_name = f"Supplier_{product_id}"
        buy_price = np.random.uniform(10, 100).round(2)
        sell_price = np.random.uniform(100, 200).round(2)
        buy_date = random_dates(now - timedelta(days=365), now)
        expiration_date = random_dates(
            now + timedelta(days=365), now + timedelta(days=365 * 2)
        )
        quantity = np.random.randint(1, 50)
        bought.append(
            [
                product_id,
                product_name,
                supplier_name,
                buy_price,
                sell_price,
                buy_date,
                expiration_date,
                quantity,
            ]
        )

    return bought


def generate_sold_data(num_products=100):
    now = pd.to_datetime("today")
    sold = []

    for _ in range(num_products):
        product_id = np.random.randint(1, 999)
        product_name = f"Product_{product_id}"
        customer_name = f"Customer_{product_id}"
        buy_date = random_dates(
            now - timedelta(days=365 * 2), now - timedelta(days=365)
        )
        buy_price = np.random.uniform(10, 100).round(2)
        expiration_date = random_dates(
            now + timedelta(days=365), now + timedelta(days=365 * 2)
        )
        sell_date = random_dates(now - timedelta(days=365), now)
        sell_price = np.random.uniform(100, 200).round(2)
        quantity = np.random.randint(1, 50)
        sold.append(
            [
                product_id,
                product_name,
                customer_name,
                buy_date,
                buy_price,
                expiration_date,
                sell_date,
                sell_price,
                quantity,
            ]
        )

    return sold


def generate_data(num_products=100, output_dir="data"):
    now = pd.to_datetime("today")

    # Generate data for inventory.csv
    inventory_data = {
        "ProductID": np.arange(1, 101),
        "ProductName": [f"Product{i}" for i in range(1, 101)],
        "Quantity": np.random.randint(1, 100, 100),
        "Price": np.random.uniform(10, 500, 100).round(2),
        "Category": np.random.choice(
            ["Electronics", "Clothing", "Grocery", "Home"], 100
        ),
        "ExpiryDate": random_dates(now, now + timedelta(days=365 * 2), 100),
        "Date": [d.date() for d in random_dates(now - timedelta(days=365), now, 100)],
        "Count": np.random.randint(1, 50, 100),
    }
    inventory_df = pd.DataFrame(inventory_data)
    inventory_df.to_csv("data/inventory.csv", index=False)

    # Generate data for expired.csv
    expired_data = {
        "ProductID": np.arange(101, 201),
        "ProductName": [f"Product{i}" for i in range(101, 201)],
        "Quantity": np.random.randint(1, 100, 100),
        "ExpiryDate": random_dates(
            now - timedelta(days=365 * 5), now - timedelta(days=365), 100
        ),
    }
    expired_df = pd.DataFrame(expired_data)
    expired_df.to_csv("data/expired.csv", index=False)

    # Assume a fixed profit margin for simplicity to generate revenue.csv and profit.csv
    margin = 0.2

    # Generate data for revenue.csv
    revenue_data = {
        "ProductID": np.arange(1, 101),
        "Revenue": (inventory_df["Price"] * inventory_df["Quantity"]).round(2),
    }
    revenue_df = pd.DataFrame(revenue_data)
    revenue_df.to_csv("data/revenue.csv", index=False)

    # Generate data for profit.csv
    profit_data = {
        "ProductID": np.arange(1, 101),
        "Profit": (revenue_df["Revenue"] * margin).round(2),
    }
    profit_df = pd.DataFrame(profit_data)
    profit_df.to_csv("data/profit.csv", index=False)

    # Generate data for bought.csv
    bought_data = {
        "id": np.arange(1, 101),
        "product": [f"Product{i}" for i in range(1, 101)],
        "name": [f"Supplier{i}" for i in range(1, 101)],
        "buy_price": np.random.uniform(10, 100, 100).round(2),
        "sell_price": np.random.uniform(100, 200, 100).round(2),
        "date": [d.date() for d in random_dates(now - timedelta(days=365), now, 100)],
        "time": [d.time() for d in random_dates(now - timedelta(days=365), now, 100)],
        "report_price": np.random.uniform(100, 200, 100).round(2),
        "expiration_date": [
            d.date()
            for d in random_dates(
                now + timedelta(days=365), now + timedelta(days=365 * 2), 100
            )
        ],
        "quantity": np.random.randint(1, 50, 100),
    }
    bought_df = pd.DataFrame(bought_data)
    bought_df.to_csv("data/bought.csv", index=False)

    # Generate data for sold.csv
    sold_data = {
        "id": np.arange(1, 101),
        "product_name": [f"Product{i}" for i in range(1, 101)],
        "name": [f"Customer{i}" for i in range(1, 101)],
        "buy_date": [
            d.date()
            for d in random_dates(
                now - timedelta(days=365 * 2), now - timedelta(days=365), 100
            )
        ],
        "buy_price": np.random.uniform(10, 100, 100).round(2),
        "expiration_date": [
            d.date()
            for d in random_dates(
                now + timedelta(days=365), now + timedelta(days=365 * 2), 100
            )
        ],
        "sell_date": [
            d.date() for d in random_dates(now - timedelta(days=365), now, 100)
        ],
        "sell_price": np.random.uniform(100, 200, 100).round(2),
        "quantity": np.random.randint(1, 50, 100),
    }
    sold_df = pd.DataFrame(sold_data)
    sold_df.to_csv("data/sold.csv", index=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate random product data.")
    parser.add_argument(
        "-n",
        "--num_products",
        type=int,
        default=100,
        help="Number of products to generate.",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        type=str,
        default="data",
        help="Directory to save the generated CSV files.",
    )
    args = parser.parse_args()

    generate_data(num_products=args.num_products, output_dir=args.output_dir)
