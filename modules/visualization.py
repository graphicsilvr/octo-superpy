import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import pandas as pd
from datetime import datetime
from rich.console import Console

console = Console()

# ===== SALES VISUALIZATIONS =====


def plot_sales_over_time(start_date=None, end_date=None, product=None):
    """Plot sales trends over time with optional product filter."""
    try:
        sold_df = pd.read_csv("data/sold.csv")

        if sold_df.empty:
            console.print("[yellow]No sales data available.[/yellow]")
            return

        # Convert dates
        sold_df["sell_date"] = pd.to_datetime(sold_df["sell_date"])

        # Filter by product if specified
        if product:
            sold_df = sold_df[
                sold_df["product_name"].str.contains(product, case=False, na=False)
            ]

        # Filter by date range
        if start_date:
            sold_df = sold_df[sold_df["sell_date"] >= pd.to_datetime(start_date)]
        if end_date:
            sold_df = sold_df[sold_df["sell_date"] <= pd.to_datetime(end_date)]

        if sold_df.empty:
            console.print("[yellow]No sales data for the specified filters.[/yellow]")
            return

        # Group by date and sum quantities
        daily_sales = (
            sold_df.groupby("sell_date")
            .agg({"quantity": "sum", "sell_price": "mean"})
            .sort_index()
        )

        # Plot
        fig, ax1 = plt.subplots(figsize=(14, 6))

        # Primary axis: Quantity
        color = "tab:blue"
        ax1.set_xlabel("Date", fontsize=11, fontweight="bold")
        ax1.set_ylabel("Units Sold", color=color, fontsize=11, fontweight="bold")
        line1 = ax1.plot(
            daily_sales.index,
            daily_sales["quantity"],
            color=color,
            marker="o",
            linewidth=2,
            label="Units Sold",
        )
        ax1.tick_params(axis="y", labelcolor=color)
        ax1.grid(True, alpha=0.3)

        # Secondary axis: Average Price
        ax2 = ax1.twinx()
        color = "tab:green"
        ax2.set_ylabel("Avg Price ($)", color=color, fontsize=11, fontweight="bold")
        line2 = ax2.plot(
            daily_sales.index,
            daily_sales["sell_price"],
            color=color,
            marker="s",
            linewidth=2,
            linestyle="--",
            label="Avg Price",
        )
        ax2.tick_params(axis="y", labelcolor=color)

        # Format x-axis
        ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
        ax1.xaxis.set_major_locator(mdates.AutoDateLocator())
        fig.autofmt_xdate(rotation=45, ha="right")

        # Title and legend
        title = "📈 Sales Over Time"
        if product:
            title += f" - {product}"
        plt.title(title, fontsize=13, fontweight="bold", pad=20)

        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc="upper left", fontsize=10)

        plt.tight_layout()
        plt.show()
        console.print("[green]✅ Chart displayed successfully[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error plotting sales: {e}[/red]")


def plot_top_products(top_n=10):
    """Visualize top-selling products by quantity and revenue."""
    try:
        sold_df = pd.read_csv("data/sold.csv")

        if sold_df.empty:
            console.print("[yellow]No sales data available.[/yellow]")
            return

        # Calculate metrics
        sold_df["revenue"] = sold_df["sell_price"] * sold_df["quantity"]
        product_stats = (
            sold_df.groupby("product_name")
            .agg({"quantity": "sum", "revenue": "sum"})
            .sort_values("revenue", ascending=False)
            .head(top_n)
        )

        # Create figure with two subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

        # Subplot 1: Units Sold
        ax1.barh(
            range(len(product_stats)),
            product_stats["quantity"],
            color="steelblue",
            alpha=0.8,
        )
        ax1.set_yticks(range(len(product_stats)))
        ax1.set_yticklabels(product_stats.index)
        ax1.set_xlabel("Units Sold", fontweight="bold")
        ax1.set_title(
            f"🏆 Top {top_n} Products by Units Sold", fontweight="bold", pad=15
        )
        ax1.invert_yaxis()
        ax1.grid(axis="x", alpha=0.3)

        # Add value labels
        for i, v in enumerate(product_stats["quantity"]):
            ax1.text(v + 1, i, str(int(v)), va="center", fontweight="bold")

        # Subplot 2: Revenue
        ax2.barh(
            range(len(product_stats)),
            product_stats["revenue"],
            color="green",
            alpha=0.8,
        )
        ax2.set_yticks(range(len(product_stats)))
        ax2.set_yticklabels(product_stats.index)
        ax2.set_xlabel("Revenue ($)", fontweight="bold")
        ax2.set_title(f"💰 Top {top_n} Products by Revenue", fontweight="bold", pad=15)
        ax2.invert_yaxis()
        ax2.grid(axis="x", alpha=0.3)

        # Add value labels
        for i, v in enumerate(product_stats["revenue"]):
            ax2.text(
                v + max(product_stats["revenue"]) * 0.01,
                i,
                f"${v:.0f}",
                va="center",
                fontweight="bold",
            )

        plt.tight_layout()
        plt.show()
        console.print("[green]✅ Chart displayed successfully[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error plotting products: {e}[/red]")


# ===== PROFIT & REVENUE VISUALIZATIONS =====


def plot_profit_vs_revenue():
    """Compare profit vs revenue by product."""
    try:
        sold_df = pd.read_csv("data/sold.csv")

        if sold_df.empty:
            console.print("[yellow]No sales data available.[/yellow]")
            return

        sold_df["revenue"] = sold_df["sell_price"] * sold_df["quantity"]
        sold_df["cost"] = sold_df["buy_price"] * sold_df["quantity"]
        sold_df["profit"] = sold_df["revenue"] - sold_df["cost"]

        summary = (
            sold_df.groupby("product_name")[["revenue", "profit"]]
            .sum()
            .nlargest(10, "revenue")
        )

        fig, ax = plt.subplots(figsize=(14, 7))
        x = range(len(summary))
        width = 0.35

        bars1 = ax.bar(
            [i - width / 2 for i in x],
            summary["revenue"],
            width,
            label="Revenue",
            color="#2ecc71",
            alpha=0.85,
        )
        bars2 = ax.bar(
            [i + width / 2 for i in x],
            summary["profit"],
            width,
            label="Profit",
            color="#f39c12",
            alpha=0.85,
        )

        ax.set_xlabel("Product", fontweight="bold", fontsize=11)
        ax.set_ylabel("Amount ($)", fontweight="bold", fontsize=11)
        ax.set_title(
            "💹 Revenue vs Profit by Product", fontweight="bold", fontsize=13, pad=15
        )
        ax.set_xticks(x)
        ax.set_xticklabels(summary.index, rotation=45, ha="right")
        ax.legend(fontsize=10, loc="upper right")
        ax.grid(axis="y", alpha=0.3)

        # Add value labels on bars
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"${height:.0f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="bold",
                )

        plt.tight_layout()
        plt.show()
        console.print("[green]✅ Chart displayed successfully[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error plotting profit vs revenue: {e}[/red]")


# ===== INVENTORY VISUALIZATIONS =====


def plot_inventory_health():
    """Show inventory levels and expiration status."""
    try:
        inventory_df = pd.read_csv("data/inventory.csv")

        if inventory_df.empty:
            console.print("[yellow]No inventory data available.[/yellow]")
            return

        # Categorize by expiration
        from modules.utils import get_current_date_time

        today = get_current_date_time().date()
        inventory_df["expiration_date"] = pd.to_datetime(
            inventory_df["expiration_date"]
        ).dt.date

        active = len(inventory_df[inventory_df["expiration_date"] > today])
        expiring_soon = len(
            inventory_df[
                (inventory_df["expiration_date"] <= today)
                & (
                    inventory_df["expiration_date"]
                    >= pd.Timestamp(today) - pd.Timedelta(days=7)
                )
            ]
        )
        expired = len(inventory_df[inventory_df["expiration_date"] < today])

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

        # Pie chart: Status distribution
        statuses = [active, expiring_soon, expired]
        labels = [
            f"Active\n({active})",
            f"Expiring Soon\n({expiring_soon})",
            f"Expired\n({expired})",
        ]
        colors = ["#2ecc71", "#f39c12", "#e74c3c"]

        ax1.pie(
            statuses,
            labels=labels,
            autopct="%1.1f%%",
            colors=colors,
            startangle=90,
            textprops={"fontweight": "bold"},
        )
        ax1.set_title(
            "📦 Inventory Status Distribution", fontweight="bold", fontsize=12, pad=15
        )

        # Bar chart: Top inventory items
        top_inventory = inventory_df.nlargest(10, "quantity")[
            ["product_name", "quantity"]
        ]
        ax2.barh(
            range(len(top_inventory)),
            top_inventory["quantity"],
            color="steelblue",
            alpha=0.8,
        )
        ax2.set_yticks(range(len(top_inventory)))
        ax2.set_yticklabels(top_inventory["product_name"])
        ax2.set_xlabel("Stock Level (Units)", fontweight="bold")
        ax2.set_title(
            "📊 Top 10 Products by Stock Level", fontweight="bold", fontsize=12, pad=15
        )
        ax2.invert_yaxis()
        ax2.grid(axis="x", alpha=0.3)

        # Add value labels
        for i, v in enumerate(top_inventory["quantity"]):
            ax2.text(v + 2, i, str(int(v)), va="center", fontweight="bold")

        plt.tight_layout()
        plt.show()
        console.print("[green]✅ Chart displayed successfully[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error plotting inventory: {e}[/red]")


def plot_sales_by_customer():
    """Visualize sales distribution by customer."""
    try:
        sold_df = pd.read_csv("data/sold.csv")

        if sold_df.empty:
            console.print("[yellow]No sales data available.[/yellow]")
            return

        sold_df["revenue"] = sold_df["sell_price"] * sold_df["quantity"]
        customer_stats = (
            sold_df.groupby("customer_name")
            .agg({"quantity": "sum", "revenue": "sum"})
            .sort_values("revenue", ascending=False)
            .head(10)
        )

        fig, ax = plt.subplots(figsize=(12, 6))
        bars = ax.bar(
            range(len(customer_stats)),
            customer_stats["revenue"],
            color="#3498db",
            alpha=0.85,
            edgecolor="black",
            linewidth=1.5,
        )

        ax.set_xticks(range(len(customer_stats)))
        ax.set_xticklabels(customer_stats.index, rotation=45, ha="right")
        ax.set_ylabel("Revenue ($)", fontweight="bold", fontsize=11)
        ax.set_title(
            "👥 Top 10 Customers by Revenue", fontweight="bold", fontsize=13, pad=15
        )
        ax.grid(axis="y", alpha=0.3)

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(
                bar.get_x() + bar.get_width() / 2.0,
                height,
                f"${height:.0f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="bold",
            )

        plt.tight_layout()
        plt.show()
        console.print("[green]✅ Chart displayed successfully[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error plotting customers: {e}[/red]")


# ===== SUMMARY DASHBOARD =====


def plot_dashboard():
    """Display a 2x2 dashboard with key metrics."""
    try:
        sold_df = pd.read_csv("data/sold.csv")
        inventory_df = pd.read_csv("data/inventory.csv")

        if sold_df.empty or inventory_df.empty:
            console.print("[yellow]Insufficient data for dashboard.[/yellow]")
            return

        # Calculate metrics
        sold_df["revenue"] = sold_df["sell_price"] * sold_df["quantity"]
        sold_df["profit"] = (sold_df["sell_price"] - sold_df["buy_price"]) * sold_df[
            "quantity"
        ]
        total_revenue = sold_df["revenue"].sum()
        total_profit = sold_df["profit"].sum()
        total_inventory_value = (
            inventory_df["quantity"] * inventory_df["buy_price"]
        ).sum()
        units_in_stock = inventory_df["quantity"].sum()

        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.3)

        # Chart 1: Top Products
        ax1 = fig.add_subplot(gs[0, 0])
        top_products = sold_df.groupby("product_name")["revenue"].sum().nlargest(5)
        ax1.bar(
            range(len(top_products)), top_products.values, color="#3498db", alpha=0.8
        )
        ax1.set_xticks(range(len(top_products)))
        ax1.set_xticklabels(top_products.index, rotation=45, ha="right")
        ax1.set_title("Top 5 Products by Revenue", fontweight="bold")
        ax1.set_ylabel("Revenue ($)")

        # Chart 2: Sales Trend
        ax2 = fig.add_subplot(gs[0, 1])
        sold_df["sell_date"] = pd.to_datetime(sold_df["sell_date"])
        daily_revenue = sold_df.groupby(sold_df["sell_date"].dt.date)["revenue"].sum()
        ax2.plot(
            daily_revenue.index,
            daily_revenue.values,
            marker="o",
            color="#2ecc71",
            linewidth=2,
        )
        ax2.fill_between(
            daily_revenue.index, daily_revenue.values, alpha=0.3, color="#2ecc71"
        )
        ax2.set_title("Daily Revenue Trend", fontweight="bold")
        ax2.set_ylabel("Revenue ($)")
        ax2.tick_params(axis="x", rotation=45)
        ax2.grid(True, alpha=0.3)

        # Chart 3: Key Metrics (Text)
        ax3 = fig.add_subplot(gs[1, 0])
        ax3.axis("off")
        metrics_text = f"""
        📊 KEY METRICS
        
        Total Revenue:       ${total_revenue:,.2f}
        Total Profit:        ${total_profit:,.2f}
        Profit Margin:       {(total_profit/total_revenue*100):.1f}%
        
        Units Sold:          {int(sold_df['quantity'].sum())}
        Avg Sale Value:      ${total_revenue/len(sold_df):.2f}
        """
        ax3.text(
            0.1,
            0.5,
            metrics_text,
            fontsize=12,
            fontfamily="monospace",
            fontweight="bold",
            verticalalignment="center",
            bbox=dict(boxstyle="round", facecolor="wheat", alpha=0.5),
        )

        # Chart 4: Inventory Status
        ax4 = fig.add_subplot(gs[1, 1])
        ax4.axis("off")
        inventory_text = f"""
        📦 INVENTORY STATUS
        
        Total Products:      {len(inventory_df)}
        Units in Stock:      {int(units_in_stock)}
        Inventory Value:     ${total_inventory_value:,.2f}
        
        Avg Stock/Product:   {units_in_stock/len(inventory_df):.1f}
        Avg Price/Unit:      ${total_inventory_value/units_in_stock:.2f}
        """
        ax4.text(
            0.1,
            0.5,
            inventory_text,
            fontsize=12,
            fontfamily="monospace",
            fontweight="bold",
            verticalalignment="center",
            bbox=dict(boxstyle="round", facecolor="lightblue", alpha=0.5),
        )

        plt.suptitle("📈 SUPERPY DASHBOARD", fontsize=16, fontweight="bold", y=0.98)
        plt.show()
        console.print("[green]✅ Dashboard displayed successfully[/green]")

    except Exception as e:
        console.print(f"[red]❌ Error displaying dashboard: {e}[/red]")
