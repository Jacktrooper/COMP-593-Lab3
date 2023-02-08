
from sys import argv, exit
import os
from datetime import date
import pandas as pd
import re
def main():
    sales_csv = get_sales_csv()
    orders_dir = create_orders_dir(sales_csv)
    process_sales_data(sales_csv, orders_dir)

# Get path of sales data CSV file from the command line
def get_sales_csv():
    # Check whether command line parameter provided
    num_params = len(argv) - 1
    if num_params >= 1:
        sales_csv = argv[1]
        if os.path.isfile(sales_csv):
            return sales_csv
        else:
            print('Error: Invalid path to sales data CSV file')
            exit(1)
    else:
        print('Error: Missing path to sales data CSV file')
        exit(1)

    # Check whether provide parameter is valid path of file
    return

# Create the directory to hold the individual order Excel sheets
def create_orders_dir(sales_csv):
    # Get directory in which sales data CSV file resides
    sales_dir = os.path.dirname(os.path.abspath(sales_csv))
    today_date = date.today().isoformat()
    orders_dir = os.path.join(sales_csv, f'Orders_{today_date}')
    # Determine the name and path of the directory to hold the order data files
    if not os.path.isdir(orders_dir):
        os.makedirs(orders_dir)

    # Create the order directory if it does not already exist
    return orders_dir

# Split the sales data into individual orders and save to Excel sheets
def process_sales_data(sales_csv, orders_dir):
    # Import the sales data from the CSV file into a DataFrame
    sales_df = pd.read_csv(sales_csv)

    # Insert a new "TOTAL PRICE" column into the DataFrame
    sales_df.insert(7, 'TOTAL PRICE', sales_df['ITEM QUANTITY'] * sales_df['ITEM PRICE'])

    # Remove columns from the DataFrame that are not needed
    sales_df.drop(columns=['ADRESS', 'CITY', 'STATE', 'POSTAL CODE', 'COUNTRY'], impace=True)

    # Group the rows in the DataFrame by order ID
    for order_id, orders_df in sales_df.groupby('ORDER ID'):

    # For each order ID:
        # Remove the "ORDER ID" column
        orders_df.drop(columns=['ORDER ID'], impace=True)

        # Sort the items by item number
        orders_df.sort_values(by='ITEM NUMBER', inplace=True)

        # Append a "GRAND TOTAL" row
        grand_total = orders_df('TOTAL PRICE').sum()
        grand_total_df = pd.DataFrame({'ITEM PRICE': ['GRAND TOTAL:'], 'TOTAL PRICE': [grand_total]})
        order_df = pd.concat([orders_df, grand_total_df])
        
        # Determine the file name and full path of the Excel sheet
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name =re.sub(r'\W', '', customer_name)
        order_file = f'Order {order_id}_{customer_name}.xlsx'
        order_path = os.path.join(orders_dir, order_file)
    
        sheet_name = f'Order #{order_id}'
        order_df.to_excel(order_path, index=False, sheet_name=sheet_name)
    
    # Export the data to an Excel sheet
    # TODO: Format the Excel sheet
    pass

if __name__ == '__main__':
    main()