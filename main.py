import pandas as pd

class ExcelReader:
    def __init__(self, src_path):
        self.df = None
        self.data = None
        self.source = src_path
        self.read_excel_sheets()
        self.consolidate_data_into_df()

    def read_excel_sheets(self):
        self.data = pd.read_excel(self.source, sheet_name=None)

    def consolidate_data_into_df(self):
        all_months_data = []
        for sheet_name, data in self.data.items():
            # Assuming the structure is consistent across all sheets: Product, Sales Units, Unit Price, Total Sales
            # Add "Month" as additional column using sheet_name
            data['Month'] = sheet_name
            all_months_data.append(data)

        self.df = pd.concat(all_months_data, ignore_index=True)

    def print_df(self):
        print(self.df)

    def get_df(self):
        return self.df

def calculate_total_sales(data):
    # Calculate total sales per product across all months
    total_sales = data.groupby('Product').agg({'Total Sales': 'sum'}).reset_index()
    total_sales.columns = ['Product', 'Total Sales']
    return total_sales


if __name__ == '__main__':
    inputpath = "./input_data/Monthly_Sales_Data.xlsx"
    reader = ExcelReader(inputpath)
    reader.print_df()
    data = reader.get_df()
    total_sales = calculate_total_sales(data)
    print(total_sales)