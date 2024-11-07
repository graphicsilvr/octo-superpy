import csv
from datetime import datetime

def read_csv(file_path):
    try:
        with open(file_path, mode='r') as file:
            return list(csv.reader(file))
    except FileNotFoundError:
        return []

def write_csv(file_path, data):
    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(data)

def generate_unique_id(file_path):
    try:
        with open(file_path, mode='r') as file:
            reader = csv.reader(file)
            id_list = [int(row[0]) for row in reader if row and row[0].isdigit()]
        return max(id_list) + 1 if id_list else 1
    except FileNotFoundError:
        return 1

def buy_product(product_name, price, expiration_date):
    try:
        purchase_id = generate_unique_id('data/bought.csv')
        new_data = [purchase_id, product_name, datetime.now().strftime('%Y-%m-%d'), price, expiration_date]
        bought_data = read_csv('data/bought.csv')
        bought_data.append(new_data)
        write_csv('data/bought.csv', bought_data)
    except FileNotFoundError:
        print("Error: File not found while trying to buy a product.")
    except ValueError as ve:
        print(f"Error: Invalid data format - {ve}")
    except Exception as e:
        print(f"An unexpected error occurred while buying a product - {e}")

def sell_product(product_name, price):
    try:
        bought_data = read_csv('data/bought.csv')
        sold_data = read_csv('data/sold.csv')

        for row in bought_data:
            if row[1] == product_name:
                sold_id = generate_unique_id('data/sold.csv')
                new_sale = [sold_id, row[0], datetime.now().strftime('%Y-%m-%d'), price]
                sold_data.append(new_sale)
                bought_data.remove(row)
                write_csv('data/sold.csv', sold_data)
                write_csv('data/bought.csv', bought_data)
                return "Sale recorded successfully"
        return "Product not in stock"
    except FileNotFoundError:
        print("Error: File not found while trying to sell a product.")
    except ValueError as ve:
        print(f"Error: Invalid data format - {ve}")
    except Exception as e:
        print(f"An unexpected error occurred while selling a product - {e}")
        
def handle_buy(args):
    # Define the file path
    inventory_file = 'inventory.csv'
    new_record = {
        'product': args.product,
        'buy-price': args.buy_price,
        'quantity': args.quantity,
        'buy-date': args.buy_date.strftime("%Y-%m-%d"),  # Converting datetime object to string
        'exp-date': args.exp_date.strftime("%Y-%m-%d"),
    }
    
    # Check if the file exists and if the product is already listed with the same buy-date
    try:
        with open(inventory_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            existing_products = [row for row in reader if row['product'] == args.product and row['buy-date'] == new_record['buy-date']]
            
    except FileNotFoundError:
        existing_products = []

    # If the product exists, you might want to update the quantity (or handle as needed)
    # For simplicity, we're just appending a new record
    with open(inventory_file, mode='a', newline='') as file:
        fieldnames = ['product', 'buy-price', 'quantity', 'buy-date', 'exp-date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        
        if not existing_products:  # Check if it's the first entry
            writer.writeheader()
            
        writer.writerow(new_record)
    
    print(f"Product {args.product} purchased on {args.buy_date.strftime('%Y-%m-%d')} added to inventory.")

def handle_sell(args):
    sales_file = 'sales.csv'
    inventory_file = 'inventory.csv'
    new_sale_record = {
        'product-name': args.product_name,
        'sell-price': args.price,
        'quantity': args.quantity,
        'date': args.date.strftime("%Y-%m-%d"),  # Assuming args.date is already a datetime object
        'customer': args.customer,
    }

    # First, update the inventory by reducing the quantity
    updated_inventory = []
    product_found = False
    try:
        with open(inventory_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['product'] == args.product_name:
                    # Assuming the inventory stores quantities as integers
                    current_quantity = int(row['quantity'])
                    if current_quantity >= args.quantity:
                        row['quantity'] = str(current_quantity - args.quantity)
                        product_found = True
                    else:
                        print(f"Not enough {args.product_name} in inventory to sell.")
                        return
                updated_inventory.append(row)
                
        if product_found:
            with open(inventory_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=reader.fieldnames)
                writer.writeheader()
                writer.writerows(updated_inventory)
        else:
            print(f"Product {args.product_name} not found in inventory.")
            return
    except FileNotFoundError:
        print("Inventory file not found.")
        return

    # Then, record the sale
    with open(sales_file, mode='a', newline='') as file:
        fieldnames = ['product-name', 'sell-price', 'quantity', 'date', 'customer']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        try:
            writer.writeheader()
        except ValueError:
            # Header already exists, so we skip writing it
            pass
        writer.writerow(new_sale_record)
    
    print(f"Sold {args.quantity} of {args.product_name} on {args.date.strftime('%Y-%m-%d')}.")

def handle_export(args):
    # Decide the export type
    if args.type == 'json':
        export_to_json(args)
    elif args.type == 'xml':
        export_to_xml(args)
    else:
        print(f"Export type {args.type} is not supported.")
    
    
def handle_report(args):
    # Decide the report type
    if args.type == 'inventory':
        generate_inventory_report(args)
    elif args.type == 'sales':
        generate_sales_report(args)
    else:
        print(f"Report type {args.type} is not supported.")

def generate_inventory_report(args):
    inventory_file = 'inventory.csv'
    print("Inventory Report")
    print("Product, Quantity, Buy Price, Buy Date, Expiration Date")
    try:
        with open(inventory_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['product']}, {row['quantity']}, {row['buy-price']}, {row['buy-date']}, {row['exp-date']}")
    except FileNotFoundError:
        print("Inventory file not found.")


def generate_sales_report(args):
    sales_file = 'sales.csv'
    print("Sales Report")
    print("Product, Quantity, Sell Price, Date, Customer")
    try:
        with open(sales_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                print(f"{row['product-name']}, {row['quantity']}, {row['sell-price']}, {row['date']}, {row['customer']}")
    except FileNotFoundError:
        print("Sales file not found.")
    
def generate_revenue_report(args):
    # Assuming profit calculation requires both inventory and sales data
    print("Revenue Report (simplified example)")
    # This function would ideally calculate profit by considering the cost of goods sold (from inventory)
    # and the revenue (from sales), but here we'll just outline the structure.
    print("This feature requires implementation based on inventory and sales data.")
    
def handle_update_price(args):
    # This function would ideally update the price of a product
    print(f"Updating the price of {args.product_name} to {args.new_price}")
    print("This feature requires implementation based on the product name.")
    
def handle_visualize(args):
    # This function would ideally visualize sales data over time
    print("Visualizing sales data over time")
    print("This feature requires implementation based on sales data.")
    
def handle_advance_time(args):
    # This function would ideally advance the current date
    print(f"Advancing the current date by {args.days} days")
    print("This feature requires implementation based on the current date.")
    
def export_to_json(args):
    # This function would ideally export data to JSON
    print(f"Exporting to JSON: {args.file}")
    print("This feature requires implementation based on the data to be exported.")
    
def export_to_xml(args):
    # This function would ideally export data to XML
    print(f"Exporting to XML: {args.file}")
    print("This feature requires implementation based on the data to be exported.")

def handle_plot(args):
    # This function would ideally plot sales over time
    print(f"Plotting sales over time for product {args.product_name}")
    print("This feature requires implementation based on sales data.")



