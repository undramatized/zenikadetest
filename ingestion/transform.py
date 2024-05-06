def calculate_total_sales(data):
    # Calculate total sales per product across all months
    total_sales = data.groupby('Product').agg({'Total Sales': 'sum'}).reset_index()
    total_sales.columns = ['Product', 'Total Sales']
    return total_sales