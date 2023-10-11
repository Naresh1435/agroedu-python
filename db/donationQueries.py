import mysql.connector
from config.sql_connect import connect_mysql

connection = connect_mysql()
cursor = connection.cursor()

def create_donation(donate_data):
    try:
        query = "INSERT INTO donate (name, email,donation,purpose,type,message,transactionId,transactionMode) VALUES (%s, %s,%s,%s,%s,%s,%s,%s)"
        values = (donate_data["name"], donate_data["email"],donate_data["donation"], donate_data['purpose'],donate_data["type"], donate_data["message"], donate_data["transactionId"],donate_data["transactionMode"])
        cursor.execute(query, values)
        connection.commit()
        return cursor.lastrowid  # Return the ID of the newly inserted row
    except mysql.connector.Error as err:
        print("Query Error creating donation:", err)
        raise err

def get_all_donations(page, limit, search, sort, order):
    try:
        query = """
            SELECT * FROM donate
            WHERE name LIKE %s
            ORDER BY %s %s
            LIMIT %s OFFSET %s
        """
        search_term = f"%{search}%"
        offset = page * limit
        values = (search_term, sort, order, limit, offset)
        cursor.execute(query, values)
        donations = cursor.fetchall()

        query = "SELECT COUNT(*) FROM donate WHERE name LIKE %s"
        cursor.execute(query, (search_term,))
        total = cursor.fetchone()[0]

        total_pages = (total + limit - 1) // limit
        return {
            "page": page + 1,
            "donations": donations,
            "total": total,
            "totalPages": total_pages,
        }
    except mysql.connector.Error as err:
        print("Query Error getting donations:", err)
        raise err

