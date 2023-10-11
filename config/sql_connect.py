import mysql.connector
from mysql.connector import errorcode
from dotenv import load_dotenv
import os



# Define your MySQL database configuration
db_config = {
    "host": os.environ.get('HOST'),
    "user": os.environ.get('DBUSERNAME'),
    "password": os.environ.get('PASSWORD'),
    "database": os.environ.get('DATABASE'),
}

# Create a function to establish a database connection
def connect_mysql():
    try:
        connection = mysql.connector.connect(**db_config)
        if connection.is_connected():
            print("MySQL Connected...")
            return connection
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Error: Access denied for user")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Error: Database does not exist")
        else:
            print("Error:", err)
    return None

