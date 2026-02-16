from modules.utils import write_csv, read_csv, get_inventory_file_path


def handle_buy(args):
    inventory_file = get_inventory_file_path("inventory.csv")
    new_record = create_buy_record(args)
    existing_products = read_csv(inventory_file)
    # Logic to check for existing products and append new record
    write_csv(inventory_file, existing_products + [new_record])
