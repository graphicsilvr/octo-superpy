import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

# Set a seed for reproducibility
np.random.seed(42)

# ===== CONFIGURATION =====
PRODUCT_CATEGORIES = [
    "Fruits",
    "Vegetables",
    "Beverages",
    "Snacks",
    "Dairy",
    "Bakery",
    "Meat",
    "Seafood",
    "Frozen",
    "Canned",
]
DATA_DIR = "data"
PROFIT_MARGIN = 0.2
NUM_PRODUCTS = 100

# ===== HELPER FUNCTIONS =====


def random_dates(start, end, n=10):
    """Generate n random dates between start and end."""
    start_u = start.value // 10**9
    end_u = end.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit="s")


def generate_product_names(num_products=100):
    """Generate realistic product names with categories."""
    products = []
    for i in range(num_products):
        category = np.random.choice(PRODUCT_CATEGORIES)
        product_id = np.random.randint(1000, 9999)
        products.append(f"{category}_{product_id}")
    return products


def ensure_data_dir():
    """Create data directory if it doesn't exist."""
    os.makedirs(DATA_DIR, exist_ok=True)


# ===== DATA GENERATION FUNCTIONS =====


def generate_inventory_data(num_products=NUM_PRODUCTS):
    """Generate current inventory with realistic expiration dates."""
    now = pd.to_datetime("today")
    product_names = generate_product_names(num_products)

    inventory_data = {
        "product_id": np.arange(1, num_products + 1),
        "product_name": product_names,
        "quantity": np.random.randint(5, 200, num_products),
        "buy_price": np.random.uniform(5, 100, num_products).round(2),
        "buy_date": [
            d.date()
            for d in random_dates(
                now - timedelta(days=180), now - timedelta(days=1), num_products
            )
        ],
        "expiration_date": [
            d.date()
            for d in random_dates(
                now + timedelta(days=1), now + timedelta(days=365 * 2), num_products
            )
        ],
    }
    return pd.DataFrame(inventory_data)


def generate_expired_data(num_expired=50):
    """Generate expired products (already past expiration)."""
    now = pd.to_datetime("today")
    product_names = generate_product_names(num_expired)

    expired_data = {
        "product_id": np.arange(1001, 1001 + num_expired),
        "product_name": product_names,
        "quantity": np.random.randint(1, 100, num_expired),
        "buy_price": np.random.uniform(5, 100, num_expired).round(2),
        "buy_date": [
            d.date()
            for d in random_dates(
                now - timedelta(days=730), now - timedelta(days=365), num_expired
            )
        ],
        "expiration_date": [
            d.date()
            for d in random_dates(
                now - timedelta(days=365), now - timedelta(days=1), num_expired
            )
        ],
    }
    return pd.DataFrame(expired_data)


def generate_bought_data(num_transactions=100):
    """Generate purchase history with consistent date logic."""
    now = pd.to_datetime("today")
    product_names = generate_product_names(num_transactions)
    suppliers = [f"Supplier_{i}" for i in range(1, num_transactions + 1)]

    # Generate buy dates in the past
    buy_dates = [
        d.date()
        for d in random_dates(
            now - timedelta(days=365 * 2), now - timedelta(days=1), num_transactions
        )
    ]
    buy_prices = np.random.uniform(5, 100, num_transactions).round(2)

    bought_data = {
        "transaction_id": np.arange(1, num_transactions + 1),
        "product_name": product_names,
        "supplier_name": suppliers,
        "buy_price": buy_prices,
        "sell_price": (buy_prices * 1.5).round(2),  # 50% markup
        "buy_date": buy_dates,
        "buy_time": [
            f"{np.random.randint(0,24):02d}:{np.random.randint(0,60):02d}:{np.random.randint(0,60):02d}"
            for _ in range(num_transactions)
        ],
        "expiration_date": [
            buy_date + timedelta(days=np.random.randint(30, 365 * 2))
            for buy_date in buy_dates
        ],
        "quantity": np.random.randint(1, 100, num_transactions),
    }
    return pd.DataFrame(bought_data)


def generate_sold_data(num_transactions=100):
    """Generate sales history with logical date constraints (sell_date >= buy_date)."""
    now = pd.to_datetime("today")
    product_names = generate_product_names(num_transactions)
    customers = [f"Customer_{i}" for i in range(1, num_transactions + 1)]

    # Generate buy dates first
    buy_dates = [
        d.date()
        for d in random_dates(
            now - timedelta(days=365 * 2), now - timedelta(days=1), num_transactions
        )
    ]
    buy_prices = np.random.uniform(5, 100, num_transactions).round(2)

    # Ensure sell_date >= buy_date (typically 1-90 days after purchase)
    sell_dates = [
        buy_date + timedelta(days=np.random.randint(0, 91)) for buy_date in buy_dates
    ]

    sold_data = {
        "transaction_id": np.arange(1, num_transactions + 1),
        "product_name": product_names,
        "customer_name": customers,
        "buy_date": buy_dates,
        "buy_price": buy_prices,
        "sell_date": sell_dates,
        "sell_price": (buy_prices * 1.5).round(2),  # 50% markup
        "expiration_date": [
            buy_date + timedelta(days=np.random.randint(30, 365 * 2))
            for buy_date in buy_dates
        ],
        "quantity": np.random.randint(1, 100, num_transactions),
    }
    return pd.DataFrame(sold_data)


def generate_revenue_data(sold_df):
    """Generate revenue summary from sales data."""
    revenue_data = {
        "product_name": sold_df["product_name"],
        "total_quantity_sold": sold_df.groupby("product_name")["quantity"].sum().values,
        "revenue": (sold_df["sell_price"] * sold_df["quantity"]).round(2).values,
    }
    return pd.DataFrame(revenue_data).drop_duplicates(subset=["product_name"])


def generate_profit_data(sold_df):
    """Generate profit summary (revenue - cost)."""
    sold_df_copy = sold_df.copy()
    sold_df_copy["profit"] = (
        sold_df_copy["quantity"]
        * (sold_df_copy["sell_price"] - sold_df_copy["buy_price"])
    ).round(2)

    profit_data = {
        "product_name": sold_df_copy["product_name"],
        "total_profit": sold_df_copy.groupby("product_name")["profit"].sum().values,
    }
    return pd.DataFrame(profit_data).drop_duplicates(subset=["product_name"])


# ===== MAIN DATA GENERATION =====


def generate_all_data():
    """Generate all CSV files."""
    ensure_data_dir()

    print("🔄 Generating inventory data...")
    inventory_df = generate_inventory_data()
    inventory_df.to_csv(f"{DATA_DIR}/inventory.csv", index=False)
    print(f"✅ Created {DATA_DIR}/inventory.csv ({len(inventory_df)} records)")

    print("🔄 Generating expired products...")
    expired_df = generate_expired_data()
    expired_df.to_csv(f"{DATA_DIR}/expired.csv", index=False)
    print(f"✅ Created {DATA_DIR}/expired.csv ({len(expired_df)} records)")

    print("🔄 Generating purchase history...")
    bought_df = generate_bought_data()
    bought_df.to_csv(f"{DATA_DIR}/bought.csv", index=False)
    print(f"✅ Created {DATA_DIR}/bought.csv ({len(bought_df)} records)")

    print("🔄 Generating sales history...")
    sold_df = generate_sold_data()
    sold_df.to_csv(f"{DATA_DIR}/sold.csv", index=False)
    print(f"✅ Created {DATA_DIR}/sold.csv ({len(sold_df)} records)")

    print("🔄 Generating revenue summary...")
    revenue_df = generate_revenue_data(sold_df)
    revenue_df.to_csv(f"{DATA_DIR}/revenue.csv", index=False)
    print(f"✅ Created {DATA_DIR}/revenue.csv ({len(revenue_df)} records)")

    print("🔄 Generating profit summary...")
    profit_df = generate_profit_data(sold_df)
    profit_df.to_csv(f"{DATA_DIR}/profit.csv", index=False)
    print(f"✅ Created {DATA_DIR}/profit.csv ({len(profit_df)} records)")

    print("\n✨ Data generation complete!")


if __name__ == "__main__":
    generate_all_data()
