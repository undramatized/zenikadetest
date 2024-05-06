#!/usr/bin/env python3
import argparse
import logging
from getpass import getpass

from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from ingestion.excelreader import ExcelReader
from mysqldb import MySQLDatabase
from mysqldb.salesdb import SalesBase, Product, SalesMonthly, SalesYearly
from ingestion.transform import calculate_total_sales

# Define Constants
INPUT_PATH = "./input_data/Monthly_Sales_Data.xlsx"
YEAR = "2023"

# Set up argument parsing
parser = argparse.ArgumentParser(description='Process sales data from an Excel file and store it in a database.')
parser.add_argument('--src', type=str, default=INPUT_PATH, help='Path to the source Excel file')
parser.add_argument('--log-level', default='INFO',
                    help='Set the logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL)')

args = parser.parse_args()

# Set the global logging configuration based on the argument
logging.basicConfig(level=getattr(logging, args.log_level.upper()))
print(f"Logging level set to: {args.log_level.upper()}")

# Interactive user inputs for database configuration
print("Please enter your database connection details:")
db_host = input("Host (default: localhost): ") or "localhost"
db_port = input("Port (default: 3306): ") or "3306"
db_user = input("Username (default: root): ") or "root"
db_password = getpass("Password (default: password): ") or "password"
db_name = input("Database name (default: sales): ") or "sales"

# Read Excel Data and calculate total sales
logging.info(f"Reading from source file: {args.src}")
reader = ExcelReader(args.src)
data = reader.get_df()
logging.info(f"Applying transformations")
total_sales = calculate_total_sales(data)

# Initialize database and create tables
logging.info(f"Creating database engine: {db_name}")
mysql = MySQLDatabase(db_name,
                      username=db_user,
                      password=db_password,
                      server=db_host,
                      port=db_port,
                      log_level=args.log_level.lower())
engine = mysql.get_engine()
logging.info(f"Creating tables in {db_name} database")
SalesBase.metadata.create_all(engine)

# Load database records
try:
    with Session(engine) as session:
        # Cache for product IDs
        product_ids = {}

        # Insert Products
        products = data['Product'].unique()
        products_cnt = 0
        logging.info(f"Loading data in Products table")
        for product_name in products:
            if product_name not in product_ids:
                product = session.query(Product).filter_by(product_name=product_name).one_or_none()
                if not product:
                    product = Product(product_name=product_name)
                    session.add(product)
                    session.flush()  # Flush to obtain the product_id immediately
                    products_cnt += 1
                # Cache product_id in memory
                product_ids[product_name] = product.product_id
        logging.info(f"{products_cnt} records inserted in Products table")

        # Insert Monthly Sales
        monthly_sales_cnt = 0
        logging.info(f"Loading data in Sales_Monthly table")
        for index, row in data.iterrows():
            product_id = product_ids[row['Product']]
            new_sale = SalesMonthly(
                product_id=product_id,
                month=row['Month'],
                year=int(YEAR),
                unit_price=row['Unit Price'],
                total_units=row['Sales Units'],
                total_sales=row['Total Sales']
            )
            # Check if the monthly sales data already exists
            exists = session.query(SalesMonthly).filter(
                SalesMonthly.product_id == new_sale.product_id,
                SalesMonthly.month == new_sale.month,
                SalesMonthly.year == new_sale.year
            ).first() is not None

            if not exists:
                session.add(new_sale)
                monthly_sales_cnt += 1
        logging.info(f"{monthly_sales_cnt} records inserted in Sales_Monthly table")

        # Insert yearly sales
        yearly_sales_cnt = 0
        logging.info(f"Loading data in Sales_Yearly table")
        for index, row in total_sales.iterrows():
            product_id = product_ids[row['Product']]
            new_yearly_sale = SalesYearly(
                product_id=product_id,
                year=int(YEAR),
                total_sales=row['Total Sales']
            )
            # Check if the yearly sales data already exists using an instance
            exists = session.query(SalesYearly).filter(
                SalesYearly.product_id == new_yearly_sale.product_id,
                SalesYearly.year == new_yearly_sale.year
            ).first() is not None

            if not exists:
                session.add(new_yearly_sale)
                yearly_sales_cnt += 1
        logging.info(f"{yearly_sales_cnt} records inserted in Sales_Yearly table")

        logging.info(f"Committing changes")
        session.commit()
        logging.info(f"Successfully committed all changes")

except SQLAlchemyError as e:
    logging.error(f"An error occurred during the database transaction: {e}")
except IntegrityError as e:
    logging.error(f"An integrity error occurred: {e}")
