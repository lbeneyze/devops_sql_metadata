import pyodbc
import re

# --------------------------------------
# This Python code will establish a connection to your SQL Server database,
# retrieve the stored procedure's definition,
# and use regular expressions to find all table names referenced in the stored procedure and its subqueries.
# The table names are stored in a set and then printed to the console.
# --------------------------------------

# Establish a connection to your SQL Server database
conn = pyodbc.connect(
    'DRIVER={SQL Server};'
    'SERVER=dwhserver-a-denhartogh.database.windows.net;'
    'DATABASE=DWH001_DENHARTOGH;'
    'UID=admin_bravinci;'
    'PWD=ZXCasdqwe123$$$;'
)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Function to retrieve the tables from the stored procedure definition
def get_nobs_line_code_from_stored_procedure(procedure_name):
    # Query the definition of the stored procedure
    query = f"SELECT OBJECT_DEFINITION(OBJECT_ID('{procedure_name}'))"
    cursor.execute(query)
    definition = cursor.fetchone()[0]

    # Count the number of lines in the stored procedure definition
    num_lines = len(definition.splitlines())

    # Text num of lines
    num_lines_txt = f"Number of lines of code in the stored procedure '{procedure_name}': {num_lines}"

    return num_lines_txt

# Function to retrieve the tables from the stored procedure definition
def get_tables_from_stored_procedure(procedure_name):
    # Retrieve the stored procedure definition
    query = f"SELECT OBJECT_DEFINITION(OBJECT_ID('{procedure_name}'))"
    cursor.execute(query)
    procedure_definition = cursor.fetchone()[0]

    procedure_definition = procedure_definition.upper()

    # Find all table names in the stored procedure definition using regular expressions
    table_names = set(re.findall(r'\bFROM\s+([^\s]+)', str(procedure_definition)))
    table_names |= set(re.findall(r'\bJOIN\s+([^\s]+)', str(procedure_definition)))

    # Retrieve the tables referenced in subqueries within the stored procedure
    for table_name in table_names.copy():
        query = f"SELECT OBJECT_DEFINITION(OBJECT_ID('{table_name}'))"
        cursor.execute(query)
        table_definition = cursor.fetchone()[0]
        subquery_table_names = set(re.findall(r'\bFROM\s+([^\s]+)', str(table_definition)))
        subquery_table_names |= set(re.findall(r'\bJOIN\s+([^\s]+)', str(table_definition)))
        table_names |= subquery_table_names

    return table_names

#Cursor for all functional production stored procedures in sql server
query = f"SELECT STP_NAME FROM MDAPEL.VW_MONITOR_09_PROCESS_FUNCTIONAL_PRODUCTION_LIST"
cursor.execute(query)

# Loop through the stored procedure names
for row in cursor.fetchall():
    procedure_name = row[0]
    #print(f"Stored Procedure: {procedure_name}")

    table_names = get_tables_from_stored_procedure(procedure_name)

    # Print the table names
    print("Tables present in the stored procedure and subqueries:")
    query = f"INSERT INTO sba011.stp_tables(NAM_STORED_PROCEDURE, NAM_TABLE) VALUES (?,?)"
    for table_name in table_names:
        cursor.execute(query, procedure_name, table_name)
        # Commit the changes to the database
        conn.commit()
        print(table_name)

# Close the cursor and connection
cursor.close()
conn.close()