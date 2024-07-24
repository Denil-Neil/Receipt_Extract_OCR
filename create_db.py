import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Fetch the environment variables
host = os.getenv('DB_HOST')
user = os.getenv('DB_USER')
password = os.getenv('DB_PASS')
database = os.getenv('DB_NAME')

# Establish the database connection
mydb = mysql.connector.connect(
    host=host,
    user=user,
    passwd=password,  # Ensure the correct password is being used
    database=database
)

# Create a cursor
my_cursor = mydb.cursor()

try:
    # Example query to show tables
    my_cursor.execute("SHOW TABLES")
    tables = my_cursor.fetchall()
    
    # Commit the transaction if necessary
    mydb.commit()

except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    # Make sure to close the cursor and the connection
    my_cursor.close()
    mydb.close()
