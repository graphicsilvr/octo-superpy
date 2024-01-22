# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# imported modules from the modules folder

import os
import json

import argparse

# In superpy.py

# Import functions from the inventory module
from modules.inventory import buy_product, sell_product

# Import functions from the reporting module
from modules.reporting import (
    report_inventory,
    report_revenue,
    generate_report,
    export_to_json,
    export_to_xml,
)

# Import functions from the time_management module
from modules.time_management import advance_time, initialize_current_date

from modules.visualization import plot_sales_over_time


# call the initialize_current_date function from the time_management module
def main():
    # Initialize the current date to today
    initialize_current_date()

    # Setup the command line interface
    parser = argparse.ArgumentParser(
        description="SuperPy - Supermarket Inventory Management"
    )
    subparsers = parser.add_subparsers(dest="command")

    # Setup for 'buy' command
    buy_parser = subparsers.add_parser("buy", help="Record a product purchase")
    buy_parser.add_argument("--product-name", required=True, help="Name of the product")
    buy_parser.add_argument(
        "--price",
        type=float,
        required=True,
        help="Price at which the product was bought",
    )
    buy_parser.add_argument(
        "--expiration-date",
        required=True,
        help="Expiration date of the product (YYYY-MM-DD)",
    )

    # Setup for 'sell' command
    sell_parser = subparsers.add_parser("sell", help="Record a product sale")
    sell_parser.add_argument(
        "--product-name", required=True, help="Name of the product sold"
    )
    sell_parser.add_argument(
        "--price", type=float, required=True, help="Price at which the product was sold"
    )

    # Setup for 'report' command
    report_parser = subparsers.add_parser("report", help="Generate a report")
    report_parser.add_argument(
        "--type", required=True, help="Type of report: inventory, revenue, or general"
    )
    report_parser.add_argument(
        "--start-date", help="Start date for the report (YYYY-MM-DD)", default=None
    )
    report_parser.add_argument(
        "--end-date", help="End date for the report (YYYY-MM-DD)", default=None
    )

    # Setup for 'advance-time' command
    advance_time_parser = subparsers.add_parser(
        "advance-time", help="Advance the current date"
    )
    advance_time_parser.add_argument(
        "--days", type=int, required=True, help="Number of days to advance"
    )

    # Setup for 'export' command
    export_parser = subparsers.add_parser("export", help="Export a report")
    export_parser.add_argument(
        "--type", required=True, help="Type of report: json or xml"
    )
    export_parser.add_argument(
        "--file", help="File to export the report to", default=None
    )

    # Setup for 'visualize' command
    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize sales data over time"
    )
    visualize_parser.add_argument(
        "--start-date",
        help="Start date for the visualization (YYYY-MM-DD)",
        default=None,
    )
    visualize_parser.add_argument(
        "--end-date", help="End date for the visualization (YYYY-MM-DD)", default=None
    )

    visualize_parser.add_argument(
        "--product-name", help="Name of the product to visualize", default=None
    )

    # Parse the command line arguments
    args = parser.parse_args()
    handle_commands(args)


# Handle the different commands
def handle_commands(args):
    if args.command == "buy":
        buy_product(args.product_name, args.price, args.expiration_date)
    elif args.command == "sell":
        sell_product(args.product_name, args.price)
    elif args.command == "report":
        # Handle different types of reports
        if args.type == "inventory":
            print(report_inventory())
        elif args.type == "revenue":
            print(report_revenue(args.start_date, args.end_date))
        elif args.type == "general":
            print(generate_report())
    elif args.command == "advance-time":
        advance_time(args.days)
    elif args.command == "export":
        # Fetch the report data based on the type of report to be exported
        report_data = (
            report_inventory()
        )  # You might want to make this dynamic based on args
        if args.type == "json":
            export_to_json(report_data, args.file)
        elif args.type == "xml":
            export_to_xml(report_data, args.file, root_tag="inventory")


# Do not change this part.
if __name__ == "__main__":
    main()
