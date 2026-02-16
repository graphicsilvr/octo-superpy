import pandas as pd
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from rich.console import Console
from rich.table import Table
from modules.utils import read_csv, get_current_date_time

console = Console()

# ===== HELPER FUNCTIONS =====


def filter_by_date(df, date_col, start_date=None, end_date=None):
    """Helper to filter DataFrames based on the project's date logic."""
    if df.empty:
        return df

    # Convert date column to datetime
    df[date_col] = pd.to_datetime(df[date_col]).dt.date

    # If no dates provided, use the simulated 'today'
    if not start_date and not end_date:
        today = get_current_date_time().date()
        return df[df[date_col] == today]

    if start_date:
        start_date = pd.to_datetime(start_date).date()
        df = df[df[date_col] >= start_date]

    if end_date:
        end_date = pd.to_datetime(end_date).date()
        df = df[df[date_col] <= end_date]

    return df


def calculate_expiration_status(df):
    """Classify products by expiration status."""
    today = get_current_date_time().date()
    df["expiration_date"] = pd.to_datetime(df["expiration_date"]).dt.date

    expired = df[df["expiration_date"] < today]
    expiring_soon = df[
        (df["expiration_date"] >= today)
        & (df["expiration_date"] <= pd.Timestamp(today) + pd.Timedelta(days=7))
    ]
    fresh = df[df["expiration_date"] > pd.Timestamp(today) + pd.Timedelta(days=7)]

    return expired, expiring_soon, fresh


# ===== INVENTORY REPORTS =====


def report_inventory(start_date=None, end_date=None):
    """Display current inventory with expiration status."""
    df = read_csv("inventory.csv")

    if df.empty:
        console.print("[yellow]No inventory records found.[/yellow]")
        return

    # Filter by buy_date if date range provided
    if start_date or end_date:
        df = filter_by_date(df, "buy_date", start_date, end_date)

    if df.empty:
        console.print(
            "[yellow]No inventory records found for the selected period.[/yellow]"
        )
        return

    # Analyze expiration status
    expired, expiring_soon, fresh = calculate_expiration_status(df)

    # Main inventory table
    table = Table(title="📦 INVENTORY REPORT", header_style="bold magenta")
    table.add_column("Product", style="cyan")
    table.add_column("Qty", justify="right", style="yellow")
    table.add_column("Buy Price", justify="right")
    table.add_column("Total Value", justify="right", style="green")
    table.add_column("Expires", style="white")

    total_value = 0
    for _, row in df.iterrows():
        value = row["quantity"] * row["buy_price"]
        total_value += value
        table.add_row(
            row["product_name"][:20],
            str(int(row["quantity"])),
            f"${row['buy_price']:.2f}",
            f"${value:.2f}",
            str(row["expiration_date"]),
        )

    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{int(df['quantity'].sum())}[/bold]",
        "",
        f"[bold green]${total_value:.2f}[/bold green]",
        "",
    )

    console.print(table)

    # Expiration alerts
    console.print("\n[bold yellow]⚠️ EXPIRATION STATUS[/bold yellow]")
    console.print(f"  🔴 Expired: {len(expired)} products")
    console.print(f"  🟡 Expiring Soon (7 days): {len(expiring_soon)} products")
    console.print(f"  🟢 Fresh Stock: {len(fresh)} products")

    # Save to CSV
    df.to_csv("data/inventory_report_last_run.csv", index=False)
    console.print("\n[dim]Report saved to data/inventory_report_last_run.csv[/dim]")


def report_expired_inventory():
    """Display only expired products."""
    df = read_csv("inventory.csv")

    if df.empty:
        console.print("[yellow]No inventory records found.[/yellow]")
        return

    today = get_current_date_time().date()
    df["expiration_date"] = pd.to_datetime(df["expiration_date"]).dt.date
    expired_df = df[df["expiration_date"] < today]

    if expired_df.empty:
        console.print("[green]✅ No expired products![/green]")
        return

    table = Table(title="🔴 EXPIRED PRODUCTS", header_style="bold red")
    table.add_column("Product", style="cyan")
    table.add_column("Qty", justify="right")
    table.add_column("Expired Date", style="red")
    table.add_column("Days Overdue", justify="right", style="bold red")

    for _, row in expired_df.iterrows():
        days_overdue = (today - row["expiration_date"]).days
        table.add_row(
            row["product_name"][:20],
            str(int(row["quantity"])),
            str(row["expiration_date"]),
            str(days_overdue),
        )

    console.print(table)


# ===== REVENUE & PROFIT REPORTS =====


def report_revenue(start_date=None, end_date=None):
    """Display sales revenue with profit analysis."""
    sold_df = read_csv("sold.csv")

    if sold_df.empty:
        console.print("[yellow]No sales records found.[/yellow]")
        return

    # Filter by sell_date
    if start_date or end_date:
        sold_df = filter_by_date(sold_df, "sell_date", start_date, end_date)

    if sold_df.empty:
        console.print(
            "[yellow]No sales records found for the selected period.[/yellow]"
        )
        return

    # Calculate revenue and profit
    sold_df["revenue"] = sold_df["sell_price"] * sold_df["quantity"]
    sold_df["cost"] = sold_df["buy_price"] * sold_df["quantity"]
    sold_df["profit"] = sold_df["revenue"] - sold_df["cost"]

    total_revenue = sold_df["revenue"].sum()
    total_cost = sold_df["cost"].sum()
    total_profit = sold_df["profit"].sum()
    profit_margin = (total_profit / total_revenue * 100) if total_revenue > 0 else 0

    # Sales by product table
    table = Table(title="💰 REVENUE REPORT", header_style="bold green")
    table.add_column("Product", style="cyan")
    table.add_column("Units", justify="right")
    table.add_column("Revenue", justify="right", style="green")
    table.add_column("Cost", justify="right")
    table.add_column("Profit", justify="right", style="bold green")

    for _, row in sold_df.iterrows():
        table.add_row(
            row["product_name"][:20],
            str(int(row["quantity"])),
            f"${row['revenue']:.2f}",
            f"${row['cost']:.2f}",
            f"${row['profit']:.2f}",
        )

    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        f"[bold]{int(sold_df['quantity'].sum())}[/bold]",
        f"[bold green]${total_revenue:.2f}[/bold green]",
        f"[bold]${total_cost:.2f}[/bold]",
        f"[bold green]${total_profit:.2f}[/bold green]",
    )

    console.print(table)

    # Summary metrics
    console.print(f"\n[bold yellow]📊 FINANCIAL SUMMARY[/bold yellow]")
    console.print(f"  Revenue:       ${total_revenue:>10.2f}")
    console.print(f"  Cost:          ${total_cost:>10.2f}")
    console.print(f"  Profit:        ${total_profit:>10.2f}")
    console.print(f"  Margin:        {profit_margin:>10.1f}%")

    # Save to CSV
    sold_df.to_csv("data/revenue_report_last_run.csv", index=False)
    console.print("\n[dim]Report saved to data/revenue_report_last_run.csv[/dim]")


def report_product_performance(top_n=10):
    """Show top performing products by revenue."""
    sold_df = read_csv("sold.csv")

    if sold_df.empty:
        console.print("[yellow]No sales records found.[/yellow]")
        return

    sold_df["revenue"] = sold_df["sell_price"] * sold_df["quantity"]

    top_products = (
        sold_df.groupby("product_name")
        .agg({"quantity": "sum", "revenue": "sum"})
        .nlargest(top_n, "revenue")
        .reset_index()
    )

    table = Table(title=f"🏆 TOP {top_n} PRODUCTS BY REVENUE", header_style="bold cyan")
    table.add_column("Rank", style="yellow")
    table.add_column("Product", style="cyan")
    table.add_column("Units Sold", justify="right")
    table.add_column("Revenue", justify="right", style="green")

    for idx, (_, row) in enumerate(top_products.iterrows(), 1):
        table.add_row(
            str(idx),
            row["product_name"][:25],
            str(int(row["quantity"])),
            f"${row['revenue']:.2f}",
        )

    console.print(table)


# ===== EXPORT FUNCTIONS =====


def export_to_json(report_type="inventory", filename="report.json"):
    """Export report data to JSON file."""
    try:
        if report_type == "inventory":
            df = read_csv("inventory.csv")
            data = {
                "report_type": "inventory",
                "timestamp": datetime.now().isoformat(),
                "total_products": len(df),
                "total_value": float((df["quantity"] * df["buy_price"]).sum()),
                "products": df.to_dict(orient="records"),
            }
        elif report_type == "revenue":
            df = read_csv("sold.csv")
            df["revenue"] = df["sell_price"] * df["quantity"]
            data = {
                "report_type": "revenue",
                "timestamp": datetime.now().isoformat(),
                "total_revenue": float(df["revenue"].sum()),
                "total_units": int(df["quantity"].sum()),
                "transactions": df.to_dict(orient="records"),
            }
        else:
            console.print("[red]Invalid report type.[/red]")
            return

        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)

        console.print(f"[green]✅ Report exported to {filename}[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error exporting to JSON: {e}[/red]")


def export_to_xml(report_type="inventory", filename="report.xml"):
    """Export report data to XML file."""
    try:
        root = ET.Element("report")
        root.set("type", report_type)
        root.set("timestamp", datetime.now().isoformat())

        if report_type == "inventory":
            df = read_csv("inventory.csv")
            for _, row in df.iterrows():
                product = ET.SubElement(root, "product")
                ET.SubElement(product, "name").text = str(row["product_name"])
                ET.SubElement(product, "quantity").text = str(int(row["quantity"]))
                ET.SubElement(product, "price").text = str(round(row["buy_price"], 2))
                ET.SubElement(product, "expiration").text = str(row["expiration_date"])

        elif report_type == "revenue":
            df = read_csv("sold.csv")
            df["revenue"] = df["sell_price"] * df["quantity"]
            for _, row in df.iterrows():
                transaction = ET.SubElement(root, "transaction")
                ET.SubElement(transaction, "product").text = str(row["product_name"])
                ET.SubElement(transaction, "quantity").text = str(int(row["quantity"]))
                ET.SubElement(transaction, "revenue").text = str(
                    round(row["revenue"], 2)
                )

        tree = ET.ElementTree(root)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        console.print(f"[green]✅ Report exported to {filename}[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error exporting to XML: {e}[/red]")
