CREATE TABLE Products (
    product_id INT AUTO_INCREMENT,
    product_name VARCHAR(255),
    PRIMARY KEY (product_id)
);

CREATE TABLE Sales (
    sale_id INT AUTO_INCREMENT,
    product_id INT,
    price DECIMAL(10, 2),
    units INT,
    total DECIMAL(10, 2),
    sale_date DATE,
    PRIMARY KEY (sale_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Sales_Monthly (
    product_id INT,
    month VARCHAR(50),
    year INT,
    unit_price DECIMAL(10, 2),
    total_units INT,
    total_sales DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);

CREATE TABLE Sales_Yearly (
    product_id INT,
    year INT,
    total_sales DECIMAL(10, 2),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);
