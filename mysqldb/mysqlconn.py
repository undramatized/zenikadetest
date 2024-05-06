import logging

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from mysqldb.salesdb import SalesBase


class MySQLConnection:
    def __init__(self, dbname, username='root', password='password', server='localhost', port='3306', log_level='info'):
        self.engine = None
        drivername = "mysqlconnector"  # Ensure that driver is installed
        self.conn_str = f"mysql+{drivername}://{username}:{password}@{server}:{port}/{dbname}"
        self.create_engine(log_level)

    def create_engine(self, log_level):
        """Create the SQLAlchemy engine using the connection string."""
        logging.debug(f"Using Connection String:{self.conn_str}")
        echo_val = True if log_level == 'debug' else False
        try:
            self.engine = create_engine(self.conn_str, echo=echo_val)
            logging.info("Database engine was created successfully.")
        except SQLAlchemyError as e:
            logging.error(f"Error creating engine: {e}")

    def get_engine(self):
        """Return the current SQLAlchemy engine."""
        return self.engine

    def execute(self, statement):
        """Execute a given SQL statement using the engine."""
        try:
            with self.engine.connect() as conn:
                logging.info(f"Executing Statement: {statement}")
                return conn.execute(text(statement)).fetchall()
        except SQLAlchemyError as e:
            logging.error(f"Error executing statement: {statement}, Error: {e}")
            return None

    def create_tables(self, base):
        try:
            base.metadata.create_all(self.engine)
            logging.info("All tables created successfully.")
        except SQLAlchemyError as e:
            logging.error(f"An error occurred: {e}")

    def drop_tables(self, base):
        try:
            base.metadata.drop_all(self.engine)
            logging.info("All tables dropped successfully.")
        except SQLAlchemyError as e:
            logging.error(f"An error occurred: {e}")


if __name__ == '__main__':
    mysql = MySQLConnection('sales')
    # result = mysql.execute("SELECT host FROM INFORMATION_SCHEMA.PROCESSLIST WHERE ID = CONNECTION_ID()")
    # print(result)
    mysql.drop_tables(SalesBase)
