import mysql.connector
from config.sql_connect import connect_mysql

connection = connect_mysql()
cursor = connection.cursor()

def create_gallery(gallery_data):
    try:
        # Create an SQL INSERT query
        insert_query = "INSERT INTO gallery (content,image) VALUES (%s, %s)"
        values = (gallery_data['content'], gallery_data['image'])  # Replace with actual data
        
        cursor.execute(insert_query, values)
        connection.commit()  # Commit the transaction

        return cursor.lastrowid  # Get the ID of the inserted row
    except mysql.connector.Error as err:
        print(f"Query Error creating gallery: {err}")
        raise err

def get_all_gallery():
    try:
        # Create an SQL SELECT query
        select_query = "SELECT * FROM gallery"
        
        cursor.execute(select_query)
        gallery = cursor.fetchall()  # Fetch all rows

        return gallery
    except mysql.connector.Error as err:
        print(f"Query Error getting gallery: {err}")
        raise err

def delete_from_gallery(id):
    try:
        # Create an SQL DELETE query
        delete_query = "DELETE FROM gallery WHERE id = %s"
        
        cursor.execute(delete_query, (id,))
        connection.commit()  # Commit the transaction

        if cursor.rowcount == 0:
            return None  # No rows were deleted
        
        return id
    except mysql.connector.Error as err:
        print(f"Query Error deleting gallery: {err}")
        raise err
