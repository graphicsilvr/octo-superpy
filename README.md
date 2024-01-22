# octo-superpy

Welcome to SuperPy, a versatile command-line tool designed to streamline your supermarket inventory management. SuperPy enables you to effortlessly track product purchases, monitor inventory status, and execute sales transactions, all from your command line.

## Installation

Begin by cloning the SuperPy repository and navigating to its root directory:

```bash
git clone [URL of the SuperPy Repository]
cd superpy
```

Ensure you have the necessary Python environment to run the application. For dependency details, refer to the `requirements.txt` file.

## Usage

To interact with SuperPy, use the `super.py` script located in the root directory. Execute the script with Python:

```bash
python super.py
```

## Commands

SuperPy supports the following commands for managing your inventory:

- `buy`: Add a new product to the inventory.
- `sell`: Execute a sale of a product from the inventory.
- `report`: Generate reports detailing the current inventory status.

## Options

SuperPy recognizes these options to tailor your command:

- `--product_name`: Specifies the product name.
- `--count`: Number of product units.
- `--buy_price`: Purchase price of the product.
- `--expiration_date`: Expiration date in YYYY-MM-DD format.
- `--action`: Defines the action (add or report).
- `--advance_time`: Moves the current date forward by a specified number of days.
- `--now`: Generates a report for the current date.
- `--yesterday`: Generates a report for yesterday's date.
- `--date`: Generates a report for a specific date in YYYY-MM-DD format.
- `--sell-price`: Selling price of the product.
- `--inventory_file`: Path to the CSV file containing inventory data.

## Examples

- Adding a product:

  ```bash
  python super.py buy --product_name apple --count 10 --buy_price 0.50 --expiration_date 2023-01-01 --inventory_file Data/Bought.csv
  ```

- Selling a product:

  ```bash
  python super.py sell --product_name apple --count 1 --sell-price 0.75 --inventory_file Data/Sold.csv
  ```

- Generating an inventory report:

  ```bash
  python super.py report --action report --inventory_file Data/Bought.csv
  ```

## Tests

To ensure SuperPy's reliability, a suite of tests is included. Run them using pytest in the root directory:

```bash
pytest
```

## License

SuperPy is made available under the MIT License. For more details, see the `LICENSE` file in the repository.

# File Structure

Superpy/
│
├── super.py                 # Main script for the CLI application
│
├── modules/                 # Python modules directory
│   ├── inventory.py         # Manages inventory operations
│   ├── reporting.py         # Generates various reports
│   └── time_management.py   # Handles date and time operations
│
├── data/                    # Data storage directory
│   ├── bought.csv           # Tracks purchased items
│   └── sold.csv             # Tracks sold items
│
├── tests/                   # Test scripts directory
│   ├── test_inventory.py    # Tests for inventory module
│   ├── test_reporting.py    # Tests for reporting module
│   └── test_time_management.py # Tests for time management module
│
├── docs/                    # Documentation directory
│   ├── USAGE.md             # Guide for using the CLI application
│   └── REPORT.md            # Technical project report
│
├── .gitignore               # Untracked files to ignore
└── README.md                # Project overview and setup instructions
