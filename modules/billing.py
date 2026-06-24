# modules/billing.py
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from modules.db_handler import load_inventory, save_inventory, log_sale, save_customer_receipt, generate_bill_id
from modules.expiry_check import get_action_rules

console = Console()

def run_billing_window():
    """Launches the interactive Point-of-Sale line checkout engine."""
    inventory = load_inventory()
    rules = get_action_rules(inventory)
    cart = {}
    
    console.print("\n[bold green]🛒 TERMINAL POS CHECKOUT ACTIVE[/bold green]")
    console.print("[dim]Type 'done' to process transaction or 'exit' to drop cart[/dim]\n")
    
    while True:
        p_id = input("Enter Product ID: ").strip()
        
        if p_id.lower() == 'done':
            if not cart:
                console.print("[yellow]⚠️ Cannot finalize an empty cart profile.[/yellow]")
                continue
            break
        elif p_id.lower() == 'exit':
            console.print("[red]❌ Transaction abandoned by cashier.[/red]")
            return

        if p_id not in inventory:
            console.print("[bold red]❌ Error: Product ID not registered in store systems.[/bold red]")
            print("\a")
            continue
            
        product = inventory[p_id]
        product_rule = rules[p_id]
        
        if not product_rule["allow_sale"]:
            console.print(f"[bold white on red] 🚨 EXPIRED INVENTORY RECORD LOCKED: {product['name']} ({product['expiry']}) [/bold white on red]")
            print("\a")
            continue

        # FIX: Calculate real-time remaining shelf stock for the prompt display
        current_cart_qty = cart.get(p_id, 0)
        real_available_stock = product["stock"] - current_cart_qty

        try:
            # Update the prompt string to show the real mathematical available stock
            qty_input = input(f"Enter quantity for '{product['name']}' (Available: {real_available_stock}): ").strip()
            qty = int(qty_input)
            if qty <= 0:
                console.print("[yellow]⚠️ Operational quantities must exceed 0 units.[/yellow]")
                continue
        except ValueError:
            console.print("[red]❌ Invalid entry parameters.[/red]")
            continue

        current_cart_qty = cart.get(p_id, 0)
        if current_cart_qty + qty > product["stock"]:
            console.print(f"[bold red]❌ Inventory shortage. Only {product['stock'] - current_cart_qty} units remain on shelf.[/bold red]")
            continue

        cart[p_id] = current_cart_qty + qty
        if product_rule["status"] == "NEAR_EXPIRY":
            console.print(f"[bold yellow]⚠️ Short Shelf Life: 30% Clearance Discount automatically mapped.[/bold yellow]")
        else:
            console.print(f"[green]✓ Added {qty}x {product['name']} to cart.[/green]")

    # --- 4. SHOW ALL CART ITEMS BEFORE GENERATING THE BILL ---
    console.print("\n[bold yellow]📋 REVIEWING STAGED SHOPPING CART ITEMS[/bold yellow]")
    cart_table = Table(box=None, width=45)
    cart_table.add_column("Item Name")
    cart_table.add_column("Qty", justify="right")
    cart_table.add_column("Base Price", justify="right")
    
    for item_id, item_qty in cart.items():
        cart_table.add_row(inventory[item_id]["name"], str(item_qty), f"₹{inventory[item_id]['price']:.2f}")
    console.print(Panel(cart_table, title="Staged Items", border_style="yellow"))

    # --- INTERACTIVE Option FOR CRM REGISTRATION AFTER CART REVIEW ---
    c_name = "WALK-IN CUSTOMER"
    c_mobile = "N/A"
    
    crm_choice = input("\nDo you want to perform Customer CRM Registration? (y/n): ").strip().lower()
    if crm_choice in ['y', 'yes']:
        console.print("[bold cyan]👤 CUSTOMER CRM REGISTRATION LAYER[/bold cyan]")
        c_name = input("Enter Customer Name: ").strip().replace(",","")  # Avoid commas in names for CSV compatibility
        c_mobile = input("Enter Customer Mobile Number: ").strip()
        if not c_name: c_name = "WALK-IN CUSTOMER"
        if not c_mobile: c_mobile = "N/A"
    else:
        console.print("[dim]Proceeding with standard anonymous checkout route...[/dim]")
        
    # --- INVOICE PROCESSING BLOCK ---
    bill_id = generate_bill_id()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    table = Table(title=f"🧾 INVOICE METRICS: {bill_id}", title_style="bold cyan", box=None, width=50)
    table.add_column("Item Summary", width=24)
    table.add_column("Qty", justify="right")
    table.add_column("Price", justify="right")
    table.add_column("Net (₹)", justify="right")

    gross_total = 0.0
    total_savings = 0.0
    
    # NEW HEADER FOR THE TEXT FILE RECEIPT
    receipt_items_text = f"{'Item Summary':<33} {'Qty':<4} {'Price':<9} {'Net Total':<9}\n"
    receipt_items_text += f"{'-'*33} {'-'*4} {'-'*9} {'-'*9}\n"

    for p_id, qty in cart.items():
        product = inventory[p_id]
        rule = rules[p_id]
        orig_price = product["price"]
        
        if rule["status"] == "NEAR_EXPIRY":
            final_price = orig_price * 0.70  # 30% markdown
            savings_row = (orig_price * 0.30) * qty
        else:
            final_price = orig_price
            savings_row = 0.0

        row_total = final_price * qty
        gross_total += row_total
        total_savings += savings_row
        
        item_label = f"{product['name']} (-30%)" if rule["status"] == "NEAR_EXPIRY" else product["name"]
        table.add_row(item_label, str(qty), f"₹{final_price:.2f}", f"₹{row_total:.2f}")
        
        # FIXED ALIGNMENT GENERATOR FOR TEXT FILES
        clean_label = item_label[:32]  # Crops the name safely if it is too long
        receipt_items_text += f"{clean_label:<33} {qty:<4} ₹{final_price:<8.2f} ₹{row_total:<8.2f}\n"
        
        inventory[p_id]["stock"] -= qty

    cgst = gross_total * 0.025
    sgst = gross_total * 0.025
    net_payable = gross_total + cgst + sgst

    table.add_section()
    table.add_row("Subtotal", "", "", f"₹{gross_total:.2f}")
    table.add_row("CGST [2.5%]", "", "", f"₹{cgst:.2f}")
    table.add_row("SGST [2.5%]", "", "", f"₹{sgst:.2f}")
    table.add_section()
    table.add_row("[bold green]NET PAYABLE AMOUNT[/bold green]", "", "", f"[bold green]₹{net_payable:.2f}[/bold green]")
    
    console.print("\n")
    console.print(Panel(table, border_style="cyan", expand=False))
    
    if total_savings > 0:
        console.print(f"[bold gold1]🎉 MARGIN ADVANTAGE: Saved customer ₹{total_savings:.2f} via auto-expiry marks.[/bold gold1]\n")

    # Save data models
    save_inventory(inventory)
    log_sale(bill_id, c_name, c_mobile, net_payable, total_savings)
    
    # Save text file copy
    file_receipt_output = (
        f"=====================================================\n"
        f"               SMART ENTERPRISE RETAIL               \n"
        f"=====================================================\n"
        f"INVOICE ID : {bill_id}\n"
        f"TIMESTAMP  : {timestamp}\n"
        f"CUSTOMER   : {c_name} | MOBILE: {c_mobile}\n"
        f"-----------------------------------------------------\n"
        f"{receipt_items_text}"
        f"-----------------------------------------------------\n"
        f"SUBTOTAL             : ₹{gross_total:.2f}\n"
        f"CGST [2.5%]          : ₹{cgst:.2f}\n"
        f"SGST [2.5%]          : ₹{sgst:.2f}\n"
        f"TOTAL CLEARANCE SAVED: ₹{total_savings:.2f}\n"
        f"-----------------------------------------------------\n"
        f"NET PAYABLE AMOUNT   : ₹{net_payable:.2f}\n"
        f"=====================================================\n"
        f"          🎯 SYSTEM AUDITED & CHECKED                \n"
        f"=====================================================\n"
    )
    
    save_customer_receipt(f"receipt_{bill_id}.txt", file_receipt_output)
    console.print(f"[dim]📁 Digital invoice file compiled: data/receipts/receipt_{bill_id}.txt[/dim]\n")