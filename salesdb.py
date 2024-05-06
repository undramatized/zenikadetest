from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship


SalesBase = declarative_base()


class Product(SalesBase):
    __tablename__ = 'products'
    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String(255), nullable=False)
    sales = relationship("Sale", back_populates="product")
    sales_monthly = relationship("SalesMonthly", back_populates="product")
    sales_yearly = relationship("SalesYearly", back_populates="product")


class Sale(SalesBase):
    __tablename__ = 'sales'
    sale_id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('products.product_id'))
    price = Column(DECIMAL(10, 2))
    units = Column(Integer)
    total = Column(DECIMAL(10, 2))
    sale_date = Column(Date)
    product = relationship("Product", back_populates="sales")


class SalesMonthly(SalesBase):
    __tablename__ = 'sales_monthly'
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    month = Column(String(50), primary_key=True)
    year = Column(Integer, primary_key=True)
    unit_price = Column(DECIMAL(10, 2))
    total_units = Column(Integer)
    total_sales = Column(DECIMAL(10, 2))
    product = relationship("Product", back_populates="sales_monthly")


class SalesYearly(SalesBase):
    __tablename__ = 'sales_yearly'
    product_id = Column(Integer, ForeignKey('products.product_id'), primary_key=True)
    year = Column(Integer, primary_key=True)
    total_sales = Column(DECIMAL(10, 2))
    product = relationship("Product", back_populates="sales_yearly")


if __name__ == '__main__':
    from mysqldb import MySQLDatabase

    mysql = MySQLDatabase('sales')
    engine = mysql.get_engine()
    SalesBase.metadata.create_all(engine)
