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


