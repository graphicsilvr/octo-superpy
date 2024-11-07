import csv
from datetime import datetime
from collections import defaultdict

import os
import json
import xml.etree.ElementTree as ET


def read_csv(file_path, skip_header=False):
    try:
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            if skip_header:
                next(reader, None)  # Skip the header row
            return list(reader)
    except FileNotFoundError:
        return []


def report_inventory():
    inventory = {}
    bought_data = read_csv("data/bought.csv", skip_header=True)

    for item in bought_data:
        product_name = item[1]
        if product_name not in inventory:
            inventory[product_name] = {
                "count": 0,
                "buy_price": float(item[3]),
                "expiration_date": item[4],
            }
        inventory[product_name]["count"] += 1

    return inventory


def report_revenue(start_date, end_date):
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")
    sold_data = read_csv("data/sold.csv", skip_header=True)
    revenue = 0

    for row in sold_data:
        if len(row) >= 3:  # Ensure row has at least 3 elements
            try:
                sale_date = datetime.strptime(row[2], "%Y-%m-%d")
                if start_date <= sale_date <= end_date:
                    revenue += float(row[3])
            except (ValueError, IndexError):
                continue  # Skip rows with invalid data or missing fields

    return revenue


def generate_report():
    bought_data = read_csv("data/bought.csv", skip_header=True)
    sold_data = read_csv("data/sold.csv", skip_header=True)

    # Calculate current inventory
    inventory = defaultdict(int)
    for row in bought_data:
        if len(row) > 1:  # Ensure row has at least 2 elements (including product name)
            product_name = row[1]
            inventory[product_name] += 1

    for row in sold_data:
        if len(row) > 1:
            product_name = row[1]
            inventory[product_name] -= 1

    # Generate report string
    report_lines = ["Inventory Report:\n", "Product Name | Quantity\n"]
    for product, quantity in inventory.items():
        report_lines.append(f"{product} | {quantity}\n")

    return "".join(report_lines)


# written this function to generate a profit report / for testing is function is working / check if this function is already used in previous project.
def generate_profit_report():
    bought_data = read_csv("data/bought.csv", skip_header=True)
    sold_data = read_csv("data/sold.csv", skip_header=True)

    # Calculate total cost of goods sold
    total_cost = sum(float(row[3]) for row in bought_data)

    # Calculate total revenue
    total_revenue = sum(float(row[3]) for row in sold_data)

    # Calculate profit
    profit = total_revenue - total_cost

    return {
        "total_cost": total_cost,
        "total_revenue": total_revenue,
        "profit": profit,
    }

    return "".join(report_lines)


def export_to_json(data, file_path):
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w") as json_file:
        json.dump(data, json_file, indent=4)


def export_to_xml(data, file_path, root_tag="report"):
    root = ET.Element(root_tag)
    for key, value in data.items():
        ET.SubElement(root, key).text = str(value)
    tree = ET.ElementTree(root)
    tree.write(file_path)
