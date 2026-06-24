# modules/db_handler.py
import os
from datetime import datetime

INVENTORY_FILE = "data/inventory.txt"
SALES_FILE = "data/sales_log.txt"
RECEIPTS_DIR = "data/receipts"

if not os.path.exists(RECEIPTS_DIR):
    os.makedirs(RECEIPTS_DIR)

def generate_bill_id():
    """Generates a professional retail transaction invoice ID."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def load_inventory():
    """Reads inventory.txt and parses data into a clean working dictionary."""
    inventory = {}
    if not os.path.exists(INVENTORY_FILE):
        return inventory
        
    with open(INVENTORY_FILE, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            try:
                p_id, name, price, expiry, stock = line.split(",")
                inventory[p_id] = {
                    "name": name,
                    "price": float(price),
                    "expiry": expiry.strip(),
                    "stock": int(stock)
                }
            except ValueError:
                continue
    return inventory

def save_inventory(inventory):
    """Saves the active inventory dictionary back to inventory.txt."""
    with open(INVENTORY_FILE, "w", encoding="utf-8") as file:
        for p_id, details in inventory.items():
            line = f"{p_id},{details['name']},{details['price']:.2f},{details['expiry']},{details['stock']}\n"
            file.write(line)

def log_sale(bill_id, customer_name, customer_mobile, total_payable, savings):
    """Appends transactions with explicit corporate schema headings to sales_log.txt."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    audit_line = f"TIMESTAMP: {timestamp}, INVOICE_NUMBER: {bill_id}, NAME: {customer_name}, MOBILE: {customer_mobile}, PAID: ₹{total_payable:.2f}, SAVED: ₹{savings:.2f}\n"
    with open(SALES_FILE, "a", encoding="utf-8") as file:
        file.write(audit_line)

def save_customer_receipt(filename, content):
    """Saves a standalone copy of the clean corporate text receipt file."""
    file_path = os.path.join(RECEIPTS_DIR, filename)
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)