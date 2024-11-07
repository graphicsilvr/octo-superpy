# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

import argparse
from datetime import datetime

from modules.inventory import (
    handle_buy,
    handle_sell,
    handle_report,
    handle_export,
    handle_visualize,
    handle_update_price,
)

from modules.reporting import (
    report_inventory,
    report_revenue,
    generate_profit_report,
    generate_report,
    export_to_json,
    export_to_xml,
)

from modules.time_management import advance_time, initialize_current_date

# have to remove the import from visualization and generate_data
from modules.visualization import (
    plot_data_over_time,
    plot_sales_over_time,
    plot_multiple_data_over_time,
    plot_inventory_over_time,
    plot_bought_over_time,
    plot_expired_over_time,
    plot_sold_over_time
)

from utils import random_dates
from prettytable import PrettyTable

table = PrettyTable()

"""
# Investigated this import
from modules.data import (
    generate_data,
    generate_inventory_data,
    generate_bought_data,
    generate_expired_data,
    generate_sold_data,
    generate_revenue_data,
    generate_profit_data,
)
"""

from utils import random_dates

from prettytable import PrettyTable

table = PrettyTable()
from generate_data import (
    generate_data,
    generate_inventory_data,
    generate_bought_data,
    generate_expired_data,
    generate_sold_data,
    generate_revenue_data,
    generate_profit_data,
)


def print_commands_table():
    from prettytable import PrettyTable
    
    # Existing table for commands
    table = PrettyTable()
    
    # Define the column names
    table.field_names = ["Command", "Description"]
    
    # Left align the text in the columns
    table.align = "l"
    
    # Add rows to the table
    commands = [
        ("buy", "Record a product purchase"),
        ("sell", "Record a product sale"),
        ("update-price", "Update the price of a product"),
        ("report", "Generate a report"),
        ("profit", "Calculate the profit"),
        ("plot", "Plot sales over time"),
        ("advance-time", "Advance the current date"),
        ("export", "Export a report"),
        ("visualize", "Visualize sales data over time"),
    ]
    
    for command, description in commands:
        table.add_row([command, description])
    
    # Print the table
    print(table)
    
    # New table for explaining data columns
    data_table = PrettyTable()
    
    # Define the column names
    data_table.field_names = ["Dataset", "Columns"]
    
    # Left align the text in the columns
    data_table.align = "l"
    
    # Add rows to the table
    data_columns = [
        ("bought_data", "'date' and 'count' columns found"),
        ("sold_data", "'date' and 'count' columns found"),
        ("inventory_data", "'date' and 'count' columns found"),
        ("Product Data", "['ProductID', 'ProductName', 'Quantity', 'Price', 'Category', 'ExpiryDate', 'Date', 'Count', 'date', 'count']"),
        ("Sales Data", "['id', 'product', 'name', 'buy_price', 'sell_price', 'date', 'time', 'report_price', 'expiration_date', 'quantity', 'count']"),
        ("Inventory Data", "['id', 'product_name', 'name', 'buy_date', 'buy_price', 'expiration_date', 'sell_date', 'sell_price', 'quantity', 'date', 'count']"),
    ]
    
    for dataset, columns in data_columns:
        data_table.add_row([dataset, columns])
    
    # Print the data columns table
    print(data_table)


def valid_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: '{0}'.".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description="SuperPy: Inventory Management System."
    )

    # Add the --commands argument
    parser.add_argument(
        "--commands", action="store_true", help="Show a table of commands"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to execute.")

    # Buy command
    buy_parser = subparsers.add_parser("buy", help="Record a product purchase")
    buy_parser.add_argument("--product", required=True, help="Product name")
    buy_parser.add_argument(
        "--buy-price", type=float, required=True, help="Buy price per product"
    )
    buy_parser.add_argument(
        "--quantity", type=int, default=1, help="Quantity of product"
    )
    buy_parser.add_argument(
        "--buy-date",
        type=valid_date,
        required=True,
        help="Product buy date (format YYYY-MM-DD)",
    )
    buy_parser.add_argument(
        "--customer", required=True, help="Customer who sold the product"
    )
    buy_parser.add_argument(
        "--exp-date",
        type=valid_date,
        required=True,
        help="Product expiration date (format YYYY-MM-DD)",
    )

    # Sell command
    sell_parser = subparsers.add_parser("sell", help="Record a product sale")
    sell_parser.add_argument(
        "--product", required=True, help="Name of the product sold"
    )
    sell_parser.add_argument(
        "--sell-price",
        type=float,
        required=True,
        help="Price at which the product was sold",
    )
    sell_parser.add_argument(
        "--quantity", type=int, required=True, help="Quantity of the product sold"
    )
    sell_parser.add_argument(
        "--sell-date",
        type=valid_date,
        required=True,
        help="Date of the sale (format: YYYY-MM-DD)",
    )
    sell_parser.add_argument(
        "--customer", required=True, help="Customer who sold the product"
    )
    sell_parser.add_argument(
        "--exp-date",
        type=valid_date,
        required=True,
        help="Product expiration date (format YYYY-MM-DD)",
    )

    # Update price command
    update_price_parser = subparsers.add_parser(
        "update-price", help="Update the price of a product"
    )
    update_price_parser.add_argument(
        "--product", required=True, help="Name of the product to update"
    )
    update_price_parser.add_argument(
        "--new-price", type=float, required=True, help="New price of the product"
    )
    update_price_parser.add_argument(
        "--date",
        type=valid_date,
        required=True,
        help="Date of the price update (format: YYYY-MM-DD)",
    )
    update_price_parser.add_argument(
        "--exp-date",
        type=valid_date,
        required=True,
        help="Product expiration date (format YYYY-MM-DD)",
    )

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate a report")
    report_parser.add_argument(
        "--type",
        choices=["inventory", "revenue", "profit"],
        required=True,
        help="Type of report",
    )
    report_parser.add_argument(
        "--start-date",
        type=valid_date,
        help="Start date for the report (format: YYYY-MM-DD)",
    )
    report_parser.add_argument(
        "--end-date",
        type=valid_date,
        help="End date for the report (format: YYYY-MM-DD)",
    )

    # Profit command (if needed, can be merged within report command with type=profit)
    profit_parser = subparsers.add_parser("profit", help="Calculate the profit")
    profit_parser.add_argument(
        "--start-date",
        type=valid_date,
        help="Start date for the report (format: YYYY-MM-DD)",
    )
    profit_parser.add_argument(
        "--end-date",
        type=valid_date,
        help="End date for the report (format: YYYY-MM-DD)",
    )

    # Plot command
    plot_parser = subparsers.add_parser("plot", help="Plot sales over time")
    plot_parser.add_argument(
        "--start-date",
        type=valid_date,
        required=True,
        help="Start date for the plot (format: YYYY-MM-DD)",
    )
    plot_parser.add_argument(
        "--end-date",
        type=valid_date,
        required=True,
        help="End date for the plot (format: YYYY-MM-DD)",
    )
    plot_parser.add_argument("--product", help="Name of the product to plot")

    # Advance time command
    advance_time_parser = subparsers.add_parser(
        "advance-time", help="Advance the current date"
    )
    advance_time_parser.add_argument(
        "--days", type=int, required=True, help="Number of days to advance"
    )

    # Export command
    export_parser = subparsers.add_parser("export", help="Export a report")
    export_parser.add_argument(
        "--type",
        choices=["json", "xml"],
        required=True,
        help="Type of report: json or xml",
    )
    export_parser.add_argument(
        "--file", required=True, help="File to export the report to"
    )

    # Visualize command

def parse_arguments():
    parser = argparse.ArgumentParser(description="SuperPy Inventory Management")
    subparsers = parser.add_subparsers(dest="commands", help="Available commands")

    # ... existing subparsers ...

    # Visualize command
    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize sales data over time"
    )
    visualize_parser.add_argument(
        "--start-date",
        type=valid_date,
        help="Start date for the visualization (YYYY-MM-DD)",
    )
    visualize_parser.add_argument(
        "--end-date",
        type=valid_date,
        help="End date for the visualization (YYYY-MM-DD)",
    )
    visualize_parser.add_argument(
        "--product", help="Name of the product to visualize"
    )
    visualize_parser.add_argument(
        "--visualization_type",
        type=str,
        choices=["inventory", "bought", "expired", "sold", "revenue", "profit", "all"],
        help="The type of visualization to display.",
    )

    return parser.parse_args()

    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize inventory data"
    )
    visualize_parser.add_argument(
        "type",
        choices=["inventory", "bought", "expired", "sold", "revenue", "profit", "all"],
        help="Type of visualization",
    )

    return parser.parse_args()


def handle_commands(args):
    if args.command == "buy":
        handle_buy(
            args.product,
            args.buy_price,
            args.quantity,
            args.buy_date,
            args.exp_date,
            args.customer,
        )
    elif args.command == "sell":
        handle_sell(
            product=args.product,
            sell_price=args.sell_price,
            quantity=args.quantity,
            sell_date=args.sell_date,
            customer=args.customer,
            exp_date=args.exp_date,
        )
    elif args.command == "update-price":
        handle_update_price(args.product, args.new_price)
    elif args.command == "report":
        if args.type == "inventory":
            report_inventory(args.start_date, args.end_date)
        elif args.type == "revenue":
            report_revenue(args.start_date, args.end_date)
        elif args.type == "profit":
            generate_profit_report(args.start_date, args.end_date)
    elif args.command == "plot":
        plot_sales_over_time(args.start_date, args.end_date, args.product)
    elif args.command == "advance-time":
        advance_time(args.days)
    elif args.command == "export":
        if args.type == "json":
            export_to_json(args.file)
        elif args.type == "xml":
            export_to_xml(args.file)
    elif args.command == "visualize":
        handle_visualize(
            args.start_date, args.end_date, args.product, args.visualization_type
        )
    else:
        print("Unknown command. Please use --help to see all available commands.")


# example 1


def handle_visualize(start_date, end_date, product, visualization_type):
    visualization_functions = {
        "inventory": generate_inventory_data,
        "bought": generate_bought_data,
        "expired": generate_expired_data,
        "sold": generate_sold_data,
        "revenue": generate_revenue_data,
        "profit": generate_profit_data,
    }

    if visualization_type in visualization_functions:
        data = visualization_functions[visualization_type](
            start_date, end_date, product
        )
        plot_data_over_time(data)
    elif visualization_type == "all":
        data = [
            func(start_date, end_date, product)
            for func in visualization_functions.values()
        ]
        plot_multiple_data_over_time(data)
    else:
        print(
            "Unknown visualization type. Please use --help to see all available visualization types."
        )


def handle_visualize(args):
    start_date = args.start_date
    end_date = args.end_date
    product = args.product
    visualization_type = args.visualization_type

    visualization_functions = {
        "inventory": generate_inventory_data,
        "bought": generate_bought_data,
        "expired": generate_expired_data,
        "sold": generate_sold_data,
        "revenue": generate_revenue_data,
        "profit": generate_profit_data,
    }

    if visualization_type in visualization_functions:
        data = visualization_functions[visualization_type](
            start_date, end_date, product
        )
        plot_data_over_time(data)
    elif visualization_type == "all":
        data = [
            func(start_date, end_date, product)
            for func_name, func in visualization_functions.items()
            if func_name in ["inventory", "sold"]
        ]
        plot_multiple_data_over_time(data)
    else:
        print(
            "Unknown visualization type. Please use --help to see all available visualization types."
        )


def main():
    initialize_current_date()
    generate_data()  # Generate initial data

    args = parse_arguments()

    if not args.commands:
        print_commands_table()
        return

    if args.commands == "visualize":
        handle_visualize(args)
    else:
        handle_commands(args)

if __name__ == "__main__":
    print_commands_table()