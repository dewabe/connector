import sys
import os

# Add the parent directory to sys.path to find the connector module
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

from datetime import datetime
from dateutil.relativedelta import relativedelta
from connector import AutoConnector

# Now you can use the imported entities as usual

conn = AutoConnector(r'..\.venv\.env')

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
print(person)