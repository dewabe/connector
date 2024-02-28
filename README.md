# Connector

The "connector" script is a versatile Python utility designed to facilitate seamless integration with various data sources, including SQL databases, Excel files, and CSV files. It acts as an intermediary layer, enabling users to easily query, update, and manipulate data without worrying about the specifics of each data source's connection protocol. By abstracting the connection details, the script streamlines data operations, making it invaluable for data analysis, migration, and integration tasks. Its modular architecture allows for easy extension to support additional data sources in the future, making it a flexible tool for handling diverse data management requirements.

Data is loaded into a Pandas DataFrame for easy use.

# Supported data sources

- SQL, tested MSSQL

# Installation

```sh
pip install git+https://github.com/dewabe/connector.git
```

## Usage

First, import the `AutoConnector` class from the `connector` module:

```python
from connector import AutoConnector
conn = AutoConnector(r'.env\.env')

# Execute a query
person = conn.execute_query(
    """
        SELECT
            person_name
        FROM
            persons
        WHERE
            person_number = ?
    """,
    params=(
        8,
    )
)

# Print the result
print(person)
```

Make sure to replace the path in `AutoConnector(r'.env\.env')` with the actual path to your environment or configuration file as needed. This README.md layout provides a concise introduction to your project, explains how to use your script, and provides a clear example of its functionality.