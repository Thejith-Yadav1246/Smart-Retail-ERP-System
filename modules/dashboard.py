# modules/dashboard.py
import os
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.columns import Columns
from modules.db_handler import load_inventory
from modules.expiry_check import get_action_rules

console = Console()
SALES_FILE = "data/sales_log.txt"

def calculate_business_metrics():
    """Parses structural transaction audit data lines to build live metrics."""
    total_revenue = 0.0
    total_discounts_given = 0.0
    
    if os.path.exists(SALES_FILE):
        with open(SALES_FILE, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()
                if not line or "PAID:" not in line.upper():
                    continue
                try:
                    # Break line by commas and strip surrounding whitespace
                    parts = [p.strip() for p in line.split(",")]
                    
                    paid_str = ""
                    saved_str = ""
                    
                    for part in parts:
                        if part.upper().startswith("PAID:"):
                            paid_str = part.upper().replace("PAID: ₹", "").replace("PAID:", "").strip()
                        elif part.upper().startswith("SAVED:"):
                            saved_str = part.upper().replace("SAVED: ₹", "").replace("SAVED:", "").strip()
                    
                    if paid_str:
                        total_revenue += float(paid_str)
                    if saved_str:
                        total_discounts_given += float(saved_str)
                except Exception:
                    continue

    inventory = load_inventory()
    rules = get_action_rules(inventory)
    total_expiry_loss_at_risk = 0.0
    
    for p_id, details in inventory.items():
        rule = rules[p_id]
        if rule["status"] == "EXPIRED":
            total_expiry_loss_at_risk += details["price"] * details["stock"]
            
    estimated_gross_profit = total_revenue * 0.25
    return total_revenue, total_discounts_given, total_expiry_loss_at_risk, estimated_gross_profit

def display_admin_dashboard():
    """Displays a clean corporate financial interface screen."""
    rev, discount, loss, profit = calculate_business_metrics()
    
    console.print("\n[bold magenta]📊 REAL-TIME EXECUTIVE BUSINESS INTELLIGENCE[/bold magenta]")
    console.print(f"[dim]Data Feed Active: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}[/dim]\n")
    
    card1 = Panel(f"[bold green]₹{rev:.2f}[/bold green]", title="📈 Gross Revenue", border_style="green")
    card2 = Panel(f"[bold yellow]₹{discount:.2f}[/bold yellow]", title="📉 Markdown Losses", border_style="yellow")
    card3 = Panel(f"[bold red]₹{loss:.2f}[/bold red]", title="🚨 Expired Liability", border_style="red")
    card4 = Panel(f"[bold cyan]₹{profit:.2f}[/bold cyan]", title="💼 Est. Net Profit (25%)", border_style="cyan")
    
    console.print(Columns([card1, card2, card3, card4]))
    console.print("\n")
    input("Press Enter to return to Operational Hub...")