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

### Exporting Reports
- **Export in JSON and XML Formats**: SuperPy allows you to export various reports, such as inventory data, in both JSON and XML formats for enhanced data portability and ease of use. Use the `export` command with the `--type` option set to either `json` or `xml`, along with the `--file` option to specify the destination file path. For example, `python superpy.py export --type json --file reports/inventory_report.json` exports the inventory report as a JSON file.

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

### `visualization.py` Module

The `visualization.py` module in SuperPy is responsible for creating graphical representations of various inventory data. This module plays a crucial role in providing visual insights into your inventory and sales data, making it easier to understand trends and patterns at a glance. Here are some of the key functionalities provided by the `visualization.py` module:

- **Plot Sales Over Time**: The module can generate line graphs showing sales data over a specified time period. This visualization helps in identifying peak sales periods and understanding seasonal trends.

- **Visualize Inventory Levels**: It can also display the current inventory levels over time, enabling you to track stock levels and anticipate when restocking might be necessary.

- **Compare Bought vs Sold Products**: Through visual comparison of bought and sold products, the module can assist in analyzing the turnover rate and sales efficiency.

- **Customizable Visualizations**: The module allows for customization of the visualizations based on different parameters such as date ranges, specific products, and more.

- **Interactive Graphs**: The graphs generated are interactive, allowing for closer examination of specific data points for detailed insights.

#### Using the `visualize` Command

To utilize the visualization capabilities, use the `visualize` command followed by specific arguments to tailor the output. For example:

- To visualize sales data for a specific product over a given date range, you can use:

  python superpy.py visualize --product-name "Apple" --start-date "2023-01-01" --end-date "2023-01-31"
  python superpy.py visualize --start-date "2023-01-01" --end-date "2023-01-31"
