# 📦 Octo-SuperPy v3.0

[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/)

> **Enterprise Inventory Solutions:** A high-performance management system for supermarket operations. Engineered for precision, scalability, and data-driven decision making.

---

## 📖 Table of Contents
* [What is Octo-SuperPy?](#-what-is-octo-superpy)
* [Installation & Setup](#-installation)
* [Operational Workflow](#-core-commands)
* [Analytical Reporting](#-business-reports)
* [Data Architecture](#-project-structure)

---

## 🏛️ What is Octo-SuperPy?

**Octo-SuperPy** is a comprehensive command-line application designed to modernize supermarket inventory operations. Built with Python and powered by `pandas`, `matplotlib`, and `rich`, it provides real-time inventory tracking, advanced reporting, profit analytics, and clear visualizations—right from your terminal.

It helps supermarket operators:

* **Track Purchases** — Record product acquisitions with suppliers, prices, and expiration dates.
* **Manage Sales** — Log transactions with customer information and profit calculations.
* **Monitor Stock Levels** — Real-time inventory status with expiration alerts.
* **Analyze Performance** — Revenue, profit, and product performance metrics.
* **Visualize Trends** — Beautiful charts and dashboards for data-driven decision making.
* **Simulate Time** — Internal date management for testing and forecasting.
* **Export Data** — Generate reports in JSON and XML formats for external analysis.

---

## 🚀 Installation

### Prerequisites

* **Python 3.9+**
* **pip** (Python package manager)

### Setup

1. **Clone the repository:**
```bash
git clone [URL-OF-YOUR-REPO]
cd octo-superpy-three

```


2. **Create a virtual environment (recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

```


3. **Install dependencies:**
```bash
pip install -r requirements.txt
# Or manually:
pip install pandas matplotlib rich numpy

```


4. **Generate sample data (optional):**
```bash
python -m modules.generate_data

```



### 📋 Quick Start

Run Octo-SuperPy from the root directory to see all available commands:

```bash
python superpy.py --help

```

---

## 🎯 Core Commands

### 1) Buy — Record Product Purchases

Purchase inventory from suppliers:

```bash
python superpy.py buy --product "Fruits_1234" --price 0.50 --quantity 100 --exp-date 2026-12-31

```

| Option | Description |
| --- | --- |
| `--product` | **(Required)** Product name or ID |
| `--price` | **(Required)** Purchase price per unit |
| `--quantity` | Number of units (Default: 1) |
| `--exp-date` | **(Required)** Expiration date (YYYY-MM-DD) |

**Example Output:**

> ✅ Purchased: 100x Fruits_1234 (Exp: 2026-12-31)

---

### 2) Sell — Record Sales Transactions

Execute a sale and track revenue:

```bash
python superpy.py sell --product "Fruits_1234" --price 0.75 --quantity 50 --customer "John's Market"

```

| Option | Description |
| --- | --- |
| `--product` | **(Required)** Product name |
| `--price` | **(Required)** Selling price per unit |
| `--quantity` | Units sold (Default: 1) |
| `--customer` | Customer name (Default: "General") |
| `--date` | Sale date (Default: simulated today) |

**Example Output:**

> ✅ Sold: 50x Fruits_1234 to John's Market @ $0.75/unit
> **Revenue: $37.50 | Profit: $12.50**

---

### 3) Update Price — Correct Product Pricing

```bash
python superpy.py update-price --product "Fruits_1234" --new-price 0.65

```

---

### 4) Report — Generate Business Reports

#### 4.1 Inventory Report

View current stock levels and expiration status:

```bash
python superpy.py report --type inventory

```

**Output:**

```text
╭──────────────────────────────── INVENTORY REPORT ────────────────────────────────╮
│ Product          │ Qty  │ Buy Price │ Total Value │ Expires                      │
├──────────────────┼──────┼───────────┼─────────────┼──────────────────────────────┤
│ Fruits_1234      │ 100  │ $0.50     │ $50.00      │ 2026-12-31                   │
│ ...              │ ...  │ ...       │ ...         │ ...                          │
╰──────────────────────────────────────────────────────────────────────────────────╯

⚠️ EXPIRATION STATUS
  🔴 Expired: 2 products
  🟡 Expiring Soon (7 days): 5 products
  🟢 Fresh Stock: 93 products

---

Would you like me to apply this same table-based formatting to the **Revenue Report** and **Visualization** sections as well?

📊 FINANCIAL SUMMARY
  Revenue:       $1,250.50
  Cost:          $875.25
  Profit:        $375.25
  Margin:        30.0%

5) Visualize — Display Charts and Dashboards
Create professional visualizations of your inventory data.

5.1 Sales Over Time
python superpy.py visualize --product "Fruits_1234" --start-date 2026-01-01 --end-date 2026-01-31
Shows sales trends with dual-axis (units sold + average price):

Line chart with markers

Optional product filtering

Date range selection

5.2 Top Products
python superpy.py visualize --top-products 10
Bar charts showing:

Top products by units sold

Top products by revenue

5.3 Profit vs Revenue
python superpy.py visualize --profit-chart
Comparative bar chart for profitability analysis.

5.4 Inventory Health
python superpy.py visualize --inventory-health
Displays:

Pie chart of inventory status (active/expiring/expired)

Top products by stock level

5.5 Customer Analysis
python superpy.py visualize --customer-analysis
Shows:

Top customers by revenue

Sales distribution by customer

5.6 Dashboard
python superpy.py visualize --dashboard
Comprehensive 2x2 dashboard with:

Top products by revenue

Daily revenue trend

Key financial metrics

Inventory status summary

6) Advance Time — Simulate Date Progression
Move the internal simulation clock forward (useful for testing and forecasting):

python superpy.py advance-time --days 30
Output:

⏰ Time Jumped! Current date is now: 2026-02-01
7) Export — Save Reports to External Formats
7.1 Export to JSON
python superpy.py export --type json --report-type inventory --file report.json
7.2 Export to XML
python superpy.py export --type xml --report-type revenue --file report.xml

📊 Data Management
Supported CSV Formats
Octo-SuperPy automatically manages these files in the data/ directory:

File Purpose
inventory.csv	Current stock levels and expiration dates
bought.csv	Purchase transaction history
sold.csv	Sales transaction history
revenue.csv	Revenue summaries by product
profit.csv	Profit calculations
expired.csv	Archived expired products

🔧 Advanced Features

Date Filtering
Most report and visualization commands support date ranges:

python superpy.py report --type revenue --start-date 2026-01-01 --end-date 2026-01-31
python superpy.py visualize --start-date 2026-01-01 --end-date 2026-01-07 --product "Fruits_1234"

Product Filtering
Filter visualizations and reports by product (case-insensitive partial matching):

python superpy.py visualize --product "apple"
python superpy.py visualize --product "fruit"  # Matches "Fruits_1234", "Fruits_5678", etc.

Custom Reports
Generate specific analysis:

python superpy.py report --type revenue --top-products 15
python superpy.py report --type inventory --expired-only

📈 Use Cases

Daily Operations
python superpy.py report --type inventory
python superpy.py buy --product "Vegetables_001" --price 2.00 --quantity 50 --exp-date 2026-02-05
python superpy.py sell --product "Vegetables_001" --price 3.50 --quantity 30 --customer 
"Local Café"

Weekly Analysis
python superpy.py report --type revenue --start-date 2026-01-01 --end-date 2026-01-07
python superpy.py visualize --top-products 10

Monthly Reconciliation
python superpy.py export --type json --report-type inventory --file january_inventory.json
python superpy.py export --type xml --report-type revenue --file january_revenue.xml

Forecasting
python superpy.py advance-time --days 30
python superpy.py report --type inventory
python superpy.py advance-time --days -30

📁 Project Structure
octo-superpy-three/
├── superpy.py              # Main CLI entry point
├── requirements.txt        # Python dependencies
├── README.md               # This file
│
├── modules/
│   ├── utils.py            # Helper functions (date handling, CSV I/O)
│   ├── inventory.py        # Buy/sell/update price logic
│   ├── reporting.py        # Report generation (inventory, revenue, profit)
│   ├── visualization.py    # Chart and dashboard functions
│   └── generate_data.py    # Test data generation
│
└── data/
    ├── inventory.csv       # Current stock
    ├── bought.csv          # Purchase history
    ├── sold.csv            # Sales history
    ├── revenue.csv         # Revenue summary
    ├── profit.csv          # Profit summary
    └── expired.csv         # Expired products archive

🧪 Testing & Development
Generate Sample Data
python -m modules.generate_data
Run Tests (if available)
pytest

📦 Dependencies
Package	Purpose
pandas	Data manipulation and CSV handling
numpy	Numerical operations
matplotlib	Data visualization and charts
rich	Beautiful terminal output (tables, colors)
argparse	Command-line argument parsing

🔐 Features at a Glance
✅ Real-time Inventory Tracking — Know exactly what you have in stock
✅ Expiration Management — Alerts for expired and soon-to-expire products
✅ Profit Analysis — Detailed cost vs. revenue breakdown
✅ Sales Trends — Visualize performance over time
✅ Customer Tracking — Monitor sales by customer
✅ Data Export — JSON & XML formats for external use
✅ Time Simulation — Test scenarios with date advancement
✅ Rich CLI Interface — Beautiful, colored terminal output
✅ Date Range Filtering — Flexible reporting periods
✅ Product Filtering — Focus on specific items

🎨 Example Workflow
# 1. Check current inventory
python superpy.py report --type inventory

# 2. Record a purchase
python superpy.py buy --product "Apples" --price 0.50 --quantity 200 --exp-date 2026-02-28

# 3. Log a sale
python superpy.py sell --product "Apples" --price 0.99 --quantity 50 --customer "Market A"

# 4. View daily revenue
python superpy.py report --type revenue

# 5. Visualize trends
python superpy.py visualize --dashboard

# 6. Export for accounting
python superpy.py export --type json --report-type revenue --file daily_report.json

💡 Tips & Best Practices
Use descriptive product names — makes reports easier to read

✅ Fruits_Apples_Red

❌ P1

Enter expiration dates accurately — critical for inventory health

Format: YYYY-MM-DD

Example: 2026-12-31

Review expiration alerts weekly

python superpy.py report --type inventory
Monitor profit margins

python superpy.py visualize --profit-chart
Export reports regularly

python superpy.py export --type json --report-type revenue --file backup_$(date +%Y%m%d).json

📄 License
Octo-SuperPy is released under the MIT License. See the LICENSE file for details.

🤝 Contributing
Contributions are welcome! Please feel free to:

Report bugs

Suggest new features

Submit pull requests

📞 Support
For issues, questions, or feature requests, please open an issue in the repository.

Octo-SuperPy v3.0 — Streamline Your Supermarket Operations 🐙📦
