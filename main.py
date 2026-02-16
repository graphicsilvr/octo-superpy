import pandas as pd
import os
import datetime
from parse import Parse  # Assuming the merged Parse class is in parse.py


def main():
    # 1. Setup Parser
    parser_tool = Parse()
    args = parser_tool.parse_args()

    # 2. File paths (You can define these or get them from args)
    inventory_csv = args.inventory_file
    sales_csv = "data/sales.csv"

    # 3. Load Data
    if not os.path.exists(inventory_csv):
        # Create empty file if it doesn't exist
        df = pd.DataFrame(
            columns=["id", "product_name", "buy_price", "buy_date", "expiration_date"]
        )
        df.to_csv(inventory_csv, index=False)

    inventory_df = pd.read_csv(inventory_csv)

    # 4. EXECUTE COMMANDS
    if args.command == "buy":
        new_id = len(inventory_df) + 1
        new_row = {
            "id": new_id,
            "product_name": args.product_name,
            "buy_price": args.buy_price,
            "buy_date": args.date,
            "expiration_date": args.expiration_date,
        }
        # Add to dataframe and save
        inventory_df = pd.concat(
            [inventory_df, pd.DataFrame([new_row])], ignore_index=True
        )
        inventory_df.to_csv(inventory_csv, index=False)
        print(f"OK: Purchased {args.product_name}")

    elif args.command == "sell":
        # Check if product is in stock
        mask = inventory_df["product_name"] == args.product_name
        if not mask.any():
            print("Error: Product not in stock.")
        else:
            # Logic to remove from inventory and add to sales.csv
            # (You would drop the row from inventory_df here)
            print(f"OK: Sold {args.product_name} for {args.sell_price}")

    elif args.command == "report":
        # This uses your plot_inventory function
        from plotdata import plot_inventory

        plot_inventory(inventory_df)


if __name__ == "__main__":
    main()
