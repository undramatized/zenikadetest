import logging

from sqlalchemy import create_engine, text


class MySQLDatabase:
    def __init__(self, dbname, username='root', password='password', server='localhost', port='3306'):
        self.engine = None
        # Driver is pre-installed in program
        drivername = "mysqlconnector"
        self.conn_str = f"mysql+{drivername}://{username}:{password}@{server}:{port}/{dbname}"
        self.create_engine()

    def create_engine(self):
        self.engine = create_engine(self.conn_str, echo=True)

    def get_engine(self):
        return self.engine

    def execute(self, statement):
        conn = self.engine.connect()
        logging.info(f"Executing Statement: {statement}")
        return conn.execute(text(statement)).fetchall()

if __name__ == '__main__':
    mysql = MySQLDatabase('sales')
    result = mysql.execute("SELECT host FROM INFORMATION_SCHEMA.PROCESSLIST WHERE ID = CONNECTION_ID()")
    print(result)


    # # # Create an engine to the MySQL database
    # engine = create_engine('mysql+mysqlconnector://root:password@localhost:3306/sales')
    #
    # # Try to connect and execute a simple "SHOW TABLES" query to confirm connectivity
    # with engine.connect() as connection:
    #     result = connection.execute(text("SHOW TABLES;"))
    #     tables = [row[0] for row in result]
    #     print("Connected to the database! Tables in the database:", tables)
