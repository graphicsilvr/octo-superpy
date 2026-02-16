import argparse
from datetime import datetime
from rich.console import Console
from rich.panel import Panel

# Import consolidated modules
from modules.utils import valid_date, get_current_date_time, advance_date_time
from modules.inventory import handle_buy, handle_sell, handle_update_price
from modules.reporting import report_inventory, report_revenue
from modules.visualization import plot_sales_over_time

console = Console()


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="[bold green]Octo-SuperPy[/bold green]: 2026 Inventory Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        dest="command", required=True, help="Action to perform"
    )

    # --- Buy Command ---
    buy_p = subparsers.add_parser("buy", help="Purchase stock")
    buy_p.add_argument("--product", required=True)
    buy_p.add_argument("--price", type=float, required=True)
    buy_p.add_argument("--quantity", type=int, default=1)
    buy_p.add_argument("--exp-date", type=valid_date, required=True)

    # --- Sell Command ---
    sell_p = subparsers.add_parser("sell", help="Record a sale")
    sell_p.add_argument("--product", required=True)
    sell_p.add_argument("--price", type=float, required=True)
    sell_p.add_argument("--quantity", type=int, default=1)
    sell_p.add_argument("--customer", default="General")
    sell_p.add_argument(
        "--date", type=valid_date, help="Date of sale (defaults to simulated today)"
    )

    # --- Update Price Command (Merged from your snippet) ---
    up_p = subparsers.add_parser("update-price", help="Correct a product's price")
    up_p.add_argument("--product", required=True)
    up_p.add_argument("--new-price", type=float, required=True)

    # --- Reporting & Profit ---
    rep_p = subparsers.add_parser("report", help="Generate tables/stats")
    rep_p.add_argument(
        "--type", choices=["inventory", "revenue", "profit"], required=True
    )
    rep_p.add_argument("--start-date", type=valid_date)
    rep_p.add_argument("--end-date", type=valid_date)

    # --- Visualization (Merged from your snippet) ---
    vis_p = subparsers.add_parser("visualize", help="Plot sales data")
    vis_p.add_argument("--product", help="Filter by product name")
    vis_p.add_argument("--start-date", type=valid_date)
    vis_p.add_argument("--end-date", type=valid_date)

    # --- Export & Time Management ---
    adv_p = subparsers.add_parser("advance-time", help="Move simulation clock")
    adv_p.add_argument("--days", type=int, required=True)

    exp_p = subparsers.add_parser("export", help="Save report to file")
    exp_p.add_argument("--format", choices=["json", "xml"], required=True)
    exp_p.add_argument("--file", required=True)

    return parser.parse_args()


def handle_commands(args):
    """
    Dispatcher Logic:
    This is where the 'Interface' tells the 'Engine' what to do.
    """
    if args.command == "buy":
        handle_buy(
            args.product,
            args.price,
            args.quantity,
            get_current_date_time().date(),
            args.exp_date,
        )

    elif args.command == "sell":
        sale_date = args.date or get_current_date_time().date()
        handle_sell(args.product, args.price, sale_date, args.quantity, args.customer)

    elif args.command == "update-price":
        handle_update_price(args.product, args.new_price)

    elif args.command == "report":
        if args.type == "inventory":
            report_inventory(args.start_date, args.end_date)
        elif args.type == "revenue":
            report_revenue(args.start_date, args.end_date)

    elif args.command == "visualize":
        plot_sales_over_time(args.start_date, args.end_date, args.product)

    elif args.command == "advance-time":
        new_date = advance_date_time(args.days)
        console.print(
            f"[bold yellow]Time Jumped![/bold yellow] Current date is now: {new_date.date()}"
        )


def main():
    args = parse_arguments()
    handle_commands(args)


if __name__ == "__main__":
    main()
