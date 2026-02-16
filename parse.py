import argparse
import datetime
import pandas as pd
import sys
import os
from plotdata import plot_inventory


class Parse:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="SuperPy is a command line tool to manage your inventory."
        )
        self._add_arguments()

    def _add_arguments(self):
        # Arguments from both files merged
        self.parser.add_argument(
            "command", type=str, help="The command to run (buy, sell, report)"
        )
        self.parser.add_argument(
            "inventory_file", type=str, help="Path to the inventory CSV file"
        )
        self.parser.add_argument(
            "--product-name", type=str, help="Name of the product."
        )
        self.parser.add_argument("--count", type=int, help="Number of units.")
        self.parser.add_argument(
            "--buy-price", type=float, help="Price at which product was bought."
        )
        self.parser.add_argument(
            "--sell-price", type=float, help="Price at which product was sold."
        )
        # General price argument for backwards compatibility or generic use
        self.parser.add_argument("--price", type=float, help="Generic price field.")
        self.parser.add_argument(
            "--expiration-date", type=str, help="Expiration date (YYYY-MM-DD)."
        )
        self.parser.add_argument(
            "--action", type=str, help="Action to perform (add or report)."
        )
        self.parser.add_argument(
            "--advance-time", type=int, help="Advance time by N days."
        )
        self.parser.add_argument(
            "--now", action="store_true", help="Set date to current date."
        )
        self.parser.add_argument(
            "--yesterday", action="store_true", help="Set date to yesterday."
        )
        self.parser.add_argument("--date", type=str, help="Specify date (YYYY-MM-DD).")

    def parse_args(self, input_args=None):
        # Use sys.argv[1:] if no arguments passed (standard CLI behavior)
        args = self.parser.parse_args(input_args)

        # Validation and Formatting Logic from File 2
        self._validate_date_format(args.expiration_date)
        args.buy_price = self._format_price(args.buy_price)
        args.sell_price = self._format_price(args.sell_price)
        args.price = self._format_price(args.price)

        # Date Logic from File 1 & 2
        self._set_date_context(args)

        return args

    @staticmethod
    def _validate_date_format(date_str):
        if date_str:
            try:
                datetime.datetime.strptime(date_str, "%Y-%m-%d")
            except ValueError:
                raise argparse.ArgumentTypeError(
                    f"Invalid date format '{date_str}'. Use YYYY-MM-DD."
                )

    @staticmethod
    def _format_price(price):
        if price is not None:
            return round(float(price), 2)
        return price

    def _set_date_context(self, args):
        if args.now:
            args.date = datetime.datetime.now().strftime("%Y-%m-%d")
        elif args.yesterday:
            yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
            args.date = yesterday.strftime("%Y-%m-%d")

        if args.date is None:
            # Default to today if nothing is specified, or keep as None depending on preference
            args.date = datetime.datetime.now().strftime("%Y-%m-%d")

        if args.advance_time:
            current_dt = datetime.datetime.strptime(args.date, "%Y-%m-%d")
            new_date = current_dt + datetime.timedelta(days=args.advance_time)
            args.date = new_date.strftime("%Y-%m-%d")


def main():
    parser_tool = Parse()
    args = parser_tool.parse_args()

    # Logic from File 1: Loading data
    if not os.path.exists(args.inventory_file):
        print(f"Error: File {args.inventory_file} not found.")
        return

    inventory_df = pd.read_csv(args.inventory_file)

    # Ensure date columns are actual datetime objects for pandas
    if "expiration_date" in inventory_df.columns:
        inventory_df["expiration_date"] = pd.to_datetime(
            inventory_df["expiration_date"]
        )
    if "date" in inventory_df.columns:
        inventory_df["date"] = pd.to_datetime(inventory_df["date"])

    # Execution logic
    if args.action == "report" or args.command == "report":
        plot_inventory(inventory_df)

    print(f"Operation '{args.command}' completed for date: {args.date}")


if __name__ == "__main__":
    main()
