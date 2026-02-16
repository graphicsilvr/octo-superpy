import os
import pandas as pd
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from modules.utils import read_csv, write_csv, get_inventory_file_path
from modules.inventory import load_inventory_data as get_inventory

console = Console()

# --- Core Business Logic ---


def handle_buy(product, buy_price, quantity, buy_date, exp_date):
    """
    Logic for buying: Adds to inventory.csv.
    If product exists with SAME expiry, it averages the price and adds quantity.
    """
    df = read_csv("inventory.csv")

    # Ensure dates are strings for comparison
    b_date_str = buy_date.strftime("%Y-%m-%d")
    e_date_str = exp_date.strftime("%Y-%m-%d")

    # Match based on product name AND expiration date
    mask = (df["product_name"] == product) & (df["expiration_date"] == e_date_str)

    if not df.empty and mask.any():
        idx = df.index[mask][0]
        # Weighted average price calculation
        old_q = df.at[idx, "count"]
        old_p = df.at[idx, "buy_price"]
        new_q = old_q + quantity

        df.at[idx, "buy_price"] = ((old_q * old_p) + (quantity * buy_price)) / new_q
        df.at[idx, "count"] = new_q
    else:
        # Create new record
        new_row = pd.DataFrame(
            [
                {
                    "product_name": product,
                    "count": quantity,
                    "buy_price": buy_price,
                    "expiration_date": e_date_str,
                    "buy_date": b_date_str,
                }
            ]
        )
        df = pd.concat([df, new_row], ignore_index=True)

    write_csv(df, "inventory.csv")
    console.print(
        f"[bold green]Purchased:[/bold green] {quantity}x {product} (Exp: {e_date_str})"
    )


def handle_sell(product, price, date, quantity, customer):
    """
    Logic for selling: Removes from inventory.csv and records in sales.csv.
    Uses FIFO (First-In-First-Out) based on expiration date.
    """
    inv_df = read_csv("inventory.csv")
    sales_df = read_csv("sales.csv")

    # 1. Check if we have enough stock (not expired)
    inv_df["expiration_date"] = pd.to_datetime(inv_df["expiration_date"])
    current_stock = inv_df[inv_df["product_name"] == product].sort_values(
        "expiration_date"
    )

    total_available = current_stock["count"].sum()

    if total_available < quantity:
        console.print(
            f"[bold red]Error:[/bold red] Only {total_available} units of {product} available."
        )
        return

    # 2. Deduct quantity (FIFO Logic)
    remaining_to_sell = quantity
    for idx in current_stock.index:
        if remaining_to_sell <= 0:
            break

        available_in_batch = inv_df.at[idx, "count"]

        if available_in_batch <= remaining_to_sell:
            remaining_to_sell -= available_in_batch
            inv_df.at[idx, "count"] = 0
        else:
            inv_df.at[idx, "count"] -= remaining_to_sell
            remaining_to_sell = 0

    # Clean up zero-count rows
    inv_df = inv_df[inv_df["count"] > 0]
    inv_df["expiration_date"] = inv_df["expiration_date"].dt.strftime("%Y-%m-%d")

    # 3. Record the Sale
    new_sale = pd.DataFrame(
        [
            {
                "product_name": product,
                "sell_price": price,
                "count": quantity,
                "date": date.strftime("%Y-%m-%d"),
                "customer": customer,
            }
        ]
    )
    sales_df = pd.concat([sales_df, new_sale], ignore_index=True)

    # 4. Save both
    write_csv(inv_df, "inventory.csv")
    write_csv(sales_df, "sales.csv")
    console.print(
        f"[bold blue]Sale Recorded:[/bold blue] {quantity}x {product} sold to {customer}"
    )


def handle_update_price(product_name, new_price):
    """Updates the buy_price of an existing item (Correction logic)."""
    df = read_csv("inventory.csv")
    if product_name in df["product_name"].values:
        df.loc[df["product_name"] == product_name, "buy_price"] = new_price
        write_csv(df, "inventory.csv")
        console.print(
            f"[yellow]Price updated for {product_name} to {new_price}[/yellow]"
        )
    else:
        console.print(f"[red]Product {product_name} not found.[/red]")


# --- NEW: Report Generation Functions ---


def report_inventory(now=False, yesterday=False, specific_date=None):
    """
    Generate inventory report for specified date.

    Args:
        now: Report for today
        yesterday: Report for yesterday
        specific_date: Report for specific date (datetime object)
    """
    df = read_csv("inventory.csv")

    if df.empty:
        console.print("[yellow]No inventory data available.[/yellow]")
        return

    # Filter based on date parameter
    target_date = None
    if now:
        target_date = datetime.now().date()
    elif yesterday:
        target_date = (datetime.now() - timedelta(days=1)).date()
    elif specific_date:
        target_date = (
            specific_date.date() if hasattr(specific_date, "date") else specific_date
        )

    # Create report table
    table = Table(title="Inventory Report")
    table.add_column("Product Name", style="cyan")
    table.add_column("Quantity", style="magenta")
    table.add_column("Buy Price", style="green")
    table.add_column("Expiration Date", style="red")

    total_qty = 0
    for _, row in df.iterrows():
        table.add_row(
            str(row["product_name"]),
            str(int(row["count"])),
            f"${row['buy_price']:.2f}",
            str(row["expiration_date"]),
        )
        total_qty += row["count"]

    console.print(table)
    console.print(f"\n[bold]Total Items:[/bold] {total_qty}")

    # Save report to CSV
    filename = f"inventory_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    df.to_csv(filename, index=False)
    console.print(f"[green]Report saved to: {filename}[/green]")


def update_inventory(product_name, new_count, date=None):
    """
    Update inventory count for a specific product.

    Args:
        product_name: Name of product to update
        new_count: New quantity value
        date: Optional date (for logging)
    """
    df = read_csv("inventory.csv")

    if product_name not in df["product_name"].values:
        console.print(f"[red]Product '{product_name}' not found in inventory.[/red]")
        return

    df.loc[df["product_name"] == product_name, "count"] = new_count
    write_csv(df, "inventory.csv")

    date_str = (
        date.strftime("%Y-%m-%d") if date else datetime.now().strftime("%Y-%m-%d")
    )
    console.print(
        f"[bold yellow]Updated:[/bold yellow] {product_name} count to {new_count} ({date_str})"
    )


def check_expired_products():
    """
    Check and report expired products.
    """
    df = read_csv("inventory.csv")

    if df.empty:
        console.print("[yellow]No inventory data.[/yellow]")
        return

    today = datetime.now().date()
    df["expiration_date"] = pd.to_datetime(df["expiration_date"])
    expired = df[df["expiration_date"].dt.date <= today]

    if expired.empty:
        console.print("[green]✓ No expired products![/green]")
        return

    table = Table(title="⚠️  Expired Products", style="red")
    table.add_column("Product", style="red")
    table.add_column("Quantity", style="yellow")
    table.add_column("Expired Date", style="red")

    for _, row in expired.iterrows():
        table.add_row(
            str(row["product_name"]),
            str(int(row["count"])),
            str(row["expiration_date"].date()),
        )

    console.print(table)
