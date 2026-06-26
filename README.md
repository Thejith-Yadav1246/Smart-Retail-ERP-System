SMART RETAIL ERP SYSTEM

A Python-based Smart Retail ERP (Enterprise Resource Planning) System designed for small retail stores.
The project provides inventory management, billing, expiry monitoring, sales logging, receipt generation, and a simple business dashboard through a terminal interface.
 Features
•	 Secure login authentication
•	 Inventory management
•	 Point of Sale (POS) billing system
•	 Automatic expiry detection
•	 30% discount for near-expiry products
•	 Prevents sale of expired products
•	 Automatic receipt generation
•	 Business dashboard with revenue statistics
•	 Sales transaction logging
•	 File-based data storage
•	
 Technologies Used
•	Python 3
•	Rich (Terminal UI)
•	File Handling
•	Modular Programming
•	Date & Time Module


Installation
1. Clone the repository
https://github.com/Thejith-Yadav1246/Smart-Retail-ERP-System.git
2. Move into the project folder
cd SMART_RETAIL_ERP
3. Install the required package
pip install rich


Project Structure
SMART_RETAIL_ERP/
│
├── main.py
├── modules/
│   ├── billing.py
│   ├── dashboard.py
│   ├── db_handler.py
│   ├── expiry_check.py
│   └── __init__.py
│
├── data/
│   ├── inventory.txt
│   ├── sales_log.txt
│   └── receipts/
│
└── README.md

 Run the Project
python main.py

 Default Login Credentials
Username : admin
Password : store123

 					 Main Modules
Inventory Management
•	Loads product data
•	Updates stock after billing
•	Saves inventory automatically

Billing System
•	Add products by Product ID
•	Quantity validation
•	Automatic discount calculation
•	Receipt generation
•	Sales logging


Expiry Management
•	Detects expired products
•	Blocks expired items from sale
•	Applies 30% discount to products nearing expiry

Dashboard
Displays business insights including:
•	Total revenue
•	Total discounts provided
•	Estimated expired stock loss
•	Estimated profit

 Data Storage
The project stores information in text files:
•	inventory.txt — Product inventory
•	sales_log.txt — Transaction history
•	receipts/ — Generated customer receipts

Future Improvements
•	Database integration (SQLite/MySQL)
•	Barcode scanner support
•	Customer management
•	Employee login roles
•	GST invoice generation
•	Product search
•	Sales analytics and charts
•	Inventory alerts
•	Backup and restore functionality
•	Graphical User Interface (Tkinter/PyQt)
