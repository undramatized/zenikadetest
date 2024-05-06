import os

import pandas as pd

from transform import calculate_total_sales


class ExcelReader:
    """
    A class to read and consolidate Excel data from multiple sheets.
    """
    def __init__(self, src_path):
        self.df = None
        self.data = None
        self.validate_path(src_path)
        self.source = src_path
        self.read_excel_sheets()
        self.consolidate_data_into_df()

    def validate_path(self, path):
        """
        Check if the source Excel file exists.
        """
        if not os.path.exists(path):
            raise FileNotFoundError(f"The file {path} does not exist.")

    def read_excel_sheets(self):
        try:
            self.data = pd.read_excel(self.source, sheet_name=None)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    def consolidate_data_into_df(self):
        all_months_data = []
        for sheet_name, data in self.data.items():
            # Assuming the structure is consistent across all sheets: Product, Sales Units, Unit Price, Total Sales
            # Add "Month" as additional column using sheet_name
            data['Month'] = sheet_name
            all_months_data.append(data)

        self.df = pd.concat(all_months_data, ignore_index=True)

    def print_df(self):
        if self.df is not None:
            print(self.df)
        else:
            print("No data to display.")

    def get_df(self):
        return self.df


if __name__ == '__main__':
    inputpath = "./input_data/Monthly_Sales_Data.xlsx"
    reader = ExcelReader(inputpath)
    reader.print_df()
    data = reader.get_df()
    total_sales = calculate_total_sales(data)
    print(total_sales)

    products = data['Product'].unique()
    print(products)