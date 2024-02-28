import logging
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from .utils import load_dotenv_file


def create_db_engine(connection_string: str):
    """
    Create and return a SQLAlchemy engine instance connected to the database.

    This function initializes a database connection using SQLAlchemy's create_engine
    method, then tests the connection by opening and immediately closing it. It is
    designed to abstract the engine creation process, providing a simplified interface
    for database connections.

    Parameters:
    - connection_string (str): The database connection string in a format recognized
      by SQLAlchemy, e.g., 'postgresql://user:password@localhost/mydatabase'.

    Returns:
    - Engine: A SQLAlchemy engine instance connected to the specified database.

    Raises:
    - ValueError: If the connection string is empty or None.
    - SQLAlchemyError: If an error occurs during the creation or testing of the engine.
      This exception is from SQLAlchemy and can represent a variety of database
      connection issues, including inability to connect.
    """
    logging.info("Creating connection to database")
    if not connection_string:
        msg = "The connection string cannot be empty."
        logging.info(msg)
        raise ValueError(msg)

    try:
        engine = create_engine(connection_string)
        engine.connect().close()
        logging.info("Database connection created successfully.")
        return engine
    except SQLAlchemyError as e:
        msg = f"Failed to create database engine: {e}"
        logging.info(msg)
        raise SQLAlchemyError(msg)


def create_connection_string(db_type: str, db_server: str, db_database: str, db_username: str, db_password: str, driver: str = None) -> str:
    """
    Generate a database connection string for PostgreSQL or MSSQL from provided credentials.

    This function constructs a connection string for SQLAlchemy based on the provided
    database system, server, database name, username, and password. It supports
    PostgreSQL and MSSQL, but can be adjusted for other database systems by modifying the
    connection string format accordingly. For MSSQL, a driver can be specified to use
    with the ODBC connection.

    Parameters:
    - db_type (str): The type of the database system ('postgresql' or 'mssql').
    - db_server (str): The hostname or IP address of the database server.
    - db_database (str): The name of the database.
    - db_username (str): The username for database authentication.
    - db_password (str): The password for database authentication.
    - driver (str, optional): The ODBC driver to use for MSSQL connections. Defaults to None,
      which uses a generic driver string for demonstration.

    Returns:
    - str: A connection string that can be used with SQLAlchemy's create_engine method.

    Raises:
    - ValueError: If an unsupported database type is specified or if a driver is required but not provided for MSSQL.

    Example:
    >>> create_connection_string('postgresql', 'my_server', 'my_database', 'username', 'password')
    'postgresql://username:password@my_server/my_database'
    >>> create_connection_string('mssql', 'my_server', 'my_database', 'username', 'password', 'ODBC Driver 17 for SQL Server')
    'mssql+pyodbc://username:password@my_server/my_database?driver=ODBC+Driver+17+for+SQL+Server'
    """
    if db_type == 'postgresql':
        connection_format = "postgresql://{username}:{password}@{server}/{database}"
    elif db_type == 'mssql':
        if not driver:
            raise ValueError("A driver is required for MSSQL connections.")
        driver_string = driver.replace(' ', '+')
        connection_format = "mssql+pyodbc://{username}:{password}@{server}/{database}" + f"?driver={driver_string}"
    else:
        raise ValueError(f"Unsupported database type: {db_type}")

    return connection_format.format(username=db_username, password=db_password, server=db_server, database=db_database)



def create_connection(db_type: str, db_server: str, db_database: str, db_username: str, db_password: str, driver: str = None):
    """
    Creates and returns a SQLAlchemy engine instance connected to the specified database.

    This function abstracts the process of generating a database connection string and
    creating a SQLAlchemy engine. It supports multiple database systems, including
    PostgreSQL and MSSQL, by dynamically constructing the appropriate connection string
    with an optional driver for MSSQL and initializing the database connection.

    Parameters:
    - db_type (str): The type of the database system ('postgresql', 'mssql').
    - db_server (str): The hostname or IP address of the database server.
    - db_database (str): The name of the database.
    - db_username (str): The username for database authentication.
    - db_password (str): The password for database authentication.
    - driver (str, optional): The ODBC driver to use for MSSQL connections. Required for MSSQL.

    Returns:
    - Engine: A SQLAlchemy engine instance connected to the specified database.

    Raises:
    - ValueError: If an unsupported database type is specified, if any required parameter is missing,
                  or if a driver is required for MSSQL but not provided.
    - SQLAlchemyError: If an error occurs during the creation of the engine.
    """
    connection_string = create_connection_string(db_type, db_server, db_database, db_username, db_password, driver)

    return create_db_engine(connection_string)
