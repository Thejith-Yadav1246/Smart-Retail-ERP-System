# main.py
import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from modules.db_handler import load_inventory, save_inventory
from modules.expiry_check import get_action_rules
from modules.billing import run_billing_window
from modules.dashboard import display_admin_dashboard

console = Console()

# 1. SECURITY LOGIN MODULE GATEWAY
def run_secure_login():
    """Blocks unauthorized terminal launch behind an authentication wall."""
    os.system('cls' if os.name == 'nt' else 'clear')
    console.print("\n[bold white on navy_blue]  🔐 ERP SECURITY PROTOCOL: ENTERPRISE TERMINAL RECOGNITION  [/bold white on navy_blue]\n")
    
    attempts = 3
    while attempts > 0:
        username = input("Enter System Username: ").strip()
        password = input("Enter Security Password: ").strip()
        
        # Hardcoded Credentials
        if username == "admin" and password == "store123":
            console.print("[bold green]✓ Access Granted [/bold green]\n")
            return True
        else:
            attempts -= 1
            console.print(f"[bold red]❌ Authentication Failed! Credentials Incorrect. ({attempts} attempts left)[/bold red]\n")
            print("\a")
            
    console.print("[bold white on red]🚨 SYSTEM LOCKDOWN: Unauthorized entry attempts recorded. Terminating core execution.[/bold white on red]\n")
    sys.exit()

def execute_system_startup_audit():
    """Performs global background scanning health pass over database lines."""
    inventory = load_inventory()
    rules = get_action_rules(inventory)
    
    expired = sum(1 for p in inventory if rules[p]["status"] == "EXPIRED")
    near_expiry = sum(1 for p in inventory if rules[p]["status"] == "NEAR_EXPIRY")
    
    banner = Text()
    banner.append("⚡ SYSTEM SCAN COMPLETE: CENTRAL DATABASE AUDITED\n", style="green")
    banner.append(f"📋 Shelf Metrics Logged -> [Expired Records: {expired}] | [Near-Expiry Flagged: {near_expiry}]", style="cyan")
    
    console.print(Panel(banner, title="🏢 ENTERPRISE RESOURCE PLANNING TERMINAL", border_style="bold yellow", expand=False))
# 5. PRINT ENTIRE ACTIVE INVENTORY DUMP VIEW
def show_all_inventory_catalog():
    """Renders every single record line current in the system repository."""
    inventory = load_inventory()
    rules = get_action_rules(inventory)
    
    table = Table(title="📋 CURRENT ACTIVE OUTLET INVENTORY STOCK LISTING", title_style="bold cyan")
    table.add_column("ID", justify="center")
    table.add_column("Product Name")
    table.add_column("Price (₹)", justify="right")
    table.add_column("Expiry Date", justify="center")
    table.add_column("Stock Qty", justify="right")
    table.add_column("Operational Status", justify="center")

    sorted_inventory = sorted(inventory.items(), key=lambda x: int(x[0]))

    for p_id, d in sorted_inventory:
        status = rules[p_id]["status"]
        if status == "EXPIRED":
            status_cell = "[bold white on red] EXPIRED [/bold white on red]"
        elif status == "NEAR_EXPIRY":
            status_cell = "[bold black on yellow] NEAR EXPIRY [/bold black on yellow]"
        else:
            status_cell = "[green]SAFE / FRESH[/green]"
            
        table.add_row(p_id, d["name"], f"₹{d['price']:.2f}", d["expiry"], str(d["stock"]), status_cell)
        
    console.print(table)

# 2 & 3. COMPREHENSIVE CONTROL PROFILE: MANAGE INVENTORY WINDOW
def run_manage_inventory_hub():
    """Hosts sub-routing terminal for modifying or deleting active inventory rows."""
    while True:
        console.print("\n[bold cyan]📦 INVENTORY MANAGEMENT CONTROL PANEL[/bold cyan]")
        console.print("1. Add New Product Profile (Original Flow)")
        console.print("2. Delete / Purge Expired Products")
        console.print("3. Return to Operational Hub")
        
        sub_choice = input("\nSelect asset sub-directive (1-3): ").strip()
        inventory = load_inventory()
        
        if sub_choice == '1':
            # FIX: Fetch the absolute latest file state right before appending fields
            inventory = load_inventory()
            # Reverted back to clean original simple layout flow
            p_id = input("ID: ").strip()
            if p_id in inventory:
                console.print("[red]❌ ID already verified in files.[/red]")
                continue
            name = input("Name: ").strip().replace(",", "-")
            price = float(input("Price: "))
            expiry = input("Expiry_Date (YYYY-MM-DD): ").strip()
            stock = int(input("Stock: "))
            
            inventory[p_id] = {"name": name, "price": price, "expiry": expiry, "stock": stock}
            save_inventory(inventory)
            console.print("[green]✓ Product added successfully.[/green]")
            

        elif sub_choice == '2':
            rules = get_action_rules(inventory)
            expired_ids = [p_id for p_id in inventory if rules[p_id]["status"] == "EXPIRED"]
            
            if not expired_ids:
                console.print("[green]✓ Clean Ledger: No expired assets exist on store files.[/green]")
                continue
                
            console.print(f"[bold yellow]⚠️ Detected {len(expired_ids)} expired asset units. Processing removal commands...[/bold yellow]")
            for e_id in expired_ids:
                console.print(f"[red]🗑 Removing record: {inventory[e_id]['name']} (Expired {inventory[e_id]['expiry']})[/red]")
                del inventory[e_id]
                
            save_inventory(inventory)
            console.print("[bold green]✓ Cleanup Complete. Database tables rewritten safely.[/bold green]")
            
        elif sub_choice == '3':
            break

def main_menu():
    """Hosts primary command menu dashboard panels."""
    execute_system_startup_audit()
    
    while True:
        console.print("\n[bold white on blue]  🏬 ENTERPRISE OPERATIONAL INTERFACE CENTRAL COMMAND  [/bold white on blue]")
        console.print("1. [bold green]🛒 Execute Cashier Billing POS Session[/bold green]")
        console.print("2. [bold magenta]📊 Launch Corporate Financial Dashboard[/bold magenta]")
        console.print("3. [bold cyan]📦 Open Manage Inventory Control Hub[/bold cyan]")
        console.print("4. [bold yellow]📋 View Entire Active Product Inventory[/bold yellow]")
        console.print("5. [bold red]🔌 Terminate Active ERP Mainframe[/bold red]")
        
        choice = input("\nSelect operational window directive (1-5): ").strip()
        
        if choice == '1':
            run_billing_window()
        elif choice == '2':
            display_admin_dashboard()
        elif choice == '3':
            run_manage_inventory_hub()
        elif choice == '4':
            show_all_inventory_catalog()
        elif choice == '5':
            console.print("\n[bold yellow]✨ TERMINAL SHUTDOWN COMMAND RECOGNIZED. SYSTEM SAFE. HAVE A NICE DAY![/bold yellow]\n")
            break
        else:
            console.print("[bold red]⚠️ Selection Warning: Action parameter mapping failure.[/bold red]")

if __name__ == "__main__":
    # Launch login gateway screen immediately upon execution
    if run_secure_login():
        main_menu()