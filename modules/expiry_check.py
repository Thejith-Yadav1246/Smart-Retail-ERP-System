# modules/expiry_check.py
from datetime import datetime, date

def check_expiry_status(expiry_date_str):
    """
    Compares the expiry string (YYYY-MM-DD) with the current date.
    Returns: status string ('EXPIRED', 'NEAR_EXPIRY', 'SAFE') and days remaining.
    """
    try:
        # Convert text string from database into a real Python date object
        expiry_date = datetime.strptime(expiry_date_str.strip(), "%Y-%m-%d").date()
    except ValueError:
        return "UNKNOWN", 0

    today = date.today()
    days_left = (expiry_date - today).days

    if days_left <= 0:
        return "EXPIRED", days_left
    elif 0 < days_left <= 7:
        return "NEAR_EXPIRY", days_left
    else:
        return "SAFE", days_left

def get_action_rules(inventory):
    """
    Scans the master inventory and flags items needing discounts or blockages.
    Returns a dictionary of action rules for the POS and Dashboard.
    """
    rules = {}
    for p_id, details in inventory.items():
        status, days = check_expiry_status(details["expiry"])
        
        # Determine discount multiplier and messaging
        if status == "EXPIRED":
            discount = 1.00       # 100% off / item should be blocked from sale
            allow_sale = False
        elif status == "NEAR_EXPIRY":
            discount = 0.30       # 30% discount automatically applied
            allow_sale = True
        else:
            discount = 0.00       # Standard pricing
            allow_sale = True

        rules[p_id] = {
            "status": status,
            "days_left": days,
            "discount_multiplier": discount,
            "allow_sale": allow_sale
        }
    return rules