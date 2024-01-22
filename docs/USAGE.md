# SuperPy Usage Guide

SuperPy is a command-line supermarket inventory management application. This guide details how to use its various features, including buying and selling products, generating reports, and managing time.

## Setting Up
- Ensure Python and necessary dependencies are installed (check `requirements.txt`).
- Run `superpy.py` from the command line to start the application.

## Commands

### Buy Command
- **Usage**: `python superpy.py buy --product-name NAME --price PRICE --expiration-date DATE`
- **Description**: Record a new product purchase.
- **Parameters**:
  - `--product-name`: Name of the product.
  - `--price`: Price at which the product was bought.
  - `--expiration-date`: Expiration date of the product (format: YYYY-MM-DD).

### Sell Command
- **Usage**: `python superpy.py sell --product-name NAME --price PRICE`
- **Description**: Record a product sale.
- **Parameters**:
  - `--product-name`: Name of the product sold.
  - `--price`: Price at which the product was sold.

### Report Command
- **Usage**: `python superpy.py report --type TYPE [--start-date DATE] [--end-date DATE]`
- **Description**: Generate different types of reports.
- **Parameters**:
  - `--type`: Type of report (`inventory`, `revenue`, or `general`).
  - `--start-date`: Start date for the revenue report (optional, format: YYYY-MM-DD).
  - `--end-date`: End date for the revenue report (optional, format: YYYY-MM-DD).

### Advance Time Command
- **Usage**: `python superpy.py advance-time --days DAYS`
- **Description**: Advance the current date by a specified number of days.
- **Parameters**:
  - `--days`: Number of days to advance.

## Module Functionalities

### `inventory.py`
- Manages product purchases and sales.
- Records new purchases in `bought.csv` and updates inventory after sales.

### `reporting.py`
- Generates three types of reports:
  - Inventory Report: Current stock of products.
  - Revenue Report: Total revenue within a specified date range.
  - General Report: Overview of the inventory status.
  
### `time_management.py`
- Manages the current date of the application.
- Allows advancing the application's date to simulate time passing.