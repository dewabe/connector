# In AutoConnector you need to specify only enviroiment variable file
from connector import AutoConnector

conn = AutoConnector(r'.env')

# Do the SQL query with parameters
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
# Output
#   person_name
# 0 My Name