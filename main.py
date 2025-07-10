import pyodbc

# Database connection settings
server = "COMPUTOR\\ALEXTESTS22"  # e.g. 'localhost\\SQLEXPRESS'
database = "okay"
username = "sa"
password = "1"

# Connect to SQL Server
conn = pyodbc.connect(
    f'DRIVER={{ODBC Driver 17 for SQL Server}};'
    f'SERVER={server};'
    f'DATABASE={database};'
    f'UID={username};'
    f'PWD={password}'
)

cursor =  conn.cursor()


#MENU AND SHIT
print("Welcome to this shitty ass application.\nAttempting to connect to the database...")
try:
    cursor = db_connect()
    print("Okay i made it.")
except:
    print("Nah it did not work, bye")

userin = input("Search for a customer using the VAR number or his name:\n>")

# Your query
searchCustomerQRY = """
SELECT name, profession, vatnr, address, city, postalcode
FROM customers
WHERE vatnr LIKE ? OR name LIKE ?
"""
params = (f"%{userin}%", f"%{userin}%")
cursor.execute(searchCustomerQRY,params)

print("Your input:" + userin + "\nResult:")

# Fetch and print results
rows = cursor.fetchall()
for row in rows:
    print(row)

# Clean up
cursor.close()
conn.close()
