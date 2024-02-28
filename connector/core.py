import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from .db import create_connection
from .utils import load_dotenv_file, load_env_var


class Connector:
    """
    A database connector class for managing connections and executing SQL queries.

    This class abstracts the database connection process using SQLAlchemy and provides
    methods for performing SQL operations such as querying, inserting, updating, and deleting data.

    Attributes:
        engine (Engine): A SQLAlchemy engine instance for database operations.

    Methods:
        execute_query(query, params=None): Execute a given SQL query with optional parameters.
    """

    def __init__(self, db_type, db_server, db_database, db_username, db_password, driver=None):
        """
        Initializes the Connector with a database connection.

        Parameters:
            db_type (str): The type of the database system ('postgresql', 'mssql', etc.).
            db_server (str): The hostname or IP address of the database server.
            db_database (str): The name of the database.
            db_username (str): The username for database authentication.
            db_password (str): The password for database authentication.
            driver (str, optional): The ODBC driver to use for MSSQL connections. Required for MSSQL.

        The database connection is established based on the specified parameters,
        including the use of an appropriate driver for MSSQL connections.
        """
        self.engine = create_connection(db_type, db_server, db_database, db_username, db_password, driver)


    def execute_query(self, query, params=None):
        """
        Execute a SQL query and return the results as an iterator of pandas DataFrames, each with a specified chunksize.

        This method executes a given SQL query optionally using parameters and returns an iterator over DataFrames,
        with each DataFrame containing up to 'chunksize' rows of data. This is particularly useful for processing
        large datasets that do not fit into memory all at once.

        Parameters:
            query (str): The SQL query to execute.
            params (dict, optional): A dictionary of parameters to pass with the query. Defaults to None.

        Returns:
            Iterator of DataFrames: An iterator over DataFrames, each containing 'chunksize' rows of the query results.

        Raises:
            SQLAlchemyError: If there's an issue executing the query.
        """
        try:
            # Use pandas read_sql_query to execute the query and return an iterator over DataFrames
            return pd.read_sql_query(query, self.engine, params=params)
        except SQLAlchemyError as e:
            raise SQLAlchemyError(f"An error occurred while executing the query: {e}")


class AutoConnector(Connector):
    """
    An automated database connector class that initializes connection parameters from environment variables.

    This class extends the Connector class, automatically reading database connection parameters
    from environment variables, which are loaded from a specified .env file, to establish the database connection.

    The expected environment variables are:
    - DB_TYPE: The type of the database system ('postgresql', 'mssql', etc.).
    - DB_SERVER: The hostname or IP address of the database server.
    - DB_DATABASE: The name of the database.
    - DB_USERNAME: The username for database authentication.
    - DB_PASSWORD: The password for database authentication.
    - DB_DRIVER (optional): The database driver, required for some databases like MSSQL.

    Parameters:
    - env_file (str): The path to the .env file from which to load the environment variables.
    """

    def __init__(self, env_file: str):
        """
        Initializes the AutoConnector by reading database connection parameters from environment variables.

        Parameters:
        - env_file (str): The path to the .env file from which to load the environment variables.
        """
        # Load environment variables from a .env file
        load_dotenv_file(env_file)

        # Read database connection parameters from environment variables
        db_type = load_env_var('CONNECTOR_DB_TYPE')
        db_server = load_env_var('CONNECTOR_DB_SERVER')
        db_database = load_env_var('CONNECTOR_DB_DATABASE')
        db_username = load_env_var('CONNECTOR_DB_USERNAME')
        db_password = load_env_var('CONNECTOR_DB_PASSWORD')
        db_driver = load_env_var('CONNECTOR_DB_DRIVER') if db_type.lower() == 'mssql' else None

        # Initialize the superclass (Connector) with the environment variables, including the driver if applicable
        super().__init__(db_type, db_server, db_database, db_username, db_password, db_driver)

        