import mysql.connector
from config.sql_connect import connect_mysql

connection = connect_mysql()
cursor = connection.cursor()

def create_land_service(land_data):
    try:
        query = "INSERT INTO lands (user,landLocation,soilType,landArea,cropType,cultivationType,cultivationHistory,waterFacility,landPrice,landDesc,landImage) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s,%s)"
        values = (land_data['user'], land_data['landLocation'], land_data['soilType'],land_data['landArea'],land_data['cropType'],land_data['cultivationType'],land_data['cultivationHistroy'],land_data['waterFacility'],land_data['landPrice'],land_data['landDesc'],land_data['landImage'])
        cursor.execute(query, values)
        connection.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Query Error creating land service: {e}")

def get_all_land_services(page, limit, search, sort, order):
    try:
        query = f"SELECT * FROM lands WHERE landLocation LIKE '%{search}%' ORDER BY {sort} {order} LIMIT {limit} OFFSET {page * limit}"
        cursor.execute(query)
        result = cursor.fetchall()

        # Calculate total records (you may need to create a separate function to get total records)
        total = ...

        # Calculate total pages
        total_pages = (total + limit - 1) // limit

        return {
            "page": page + 1,
            "landService": result,
            "total": total,
            "totalPages": total_pages,
        }
    except Exception as e:
        print(f"Query Error getting land services: {e}")


def get_all_land_services_in_category(page, limit, search, sort, order, category):
    try:
        query = f"SELECT * FROM lands WHERE landLocation LIKE '%{search}%' AND cultivationType = '{category}' ORDER BY {sort} {order} LIMIT {limit} OFFSET {page * limit}"
        cursor.execute(query)
        result = cursor.fetchall()

        # Calculate total records (you may need to create a separate function to get total records)
        total = ...

        # Calculate total pages
        total_pages = (total + limit - 1) // limit

        return {
            "page": page + 1,
            "lands": result,
            "total": total,
            "totalPages": total_pages,
        }
    except Exception as e:
        print(f"Query Error getting category land services: {e}")

def get_land_service_by_id(id):
    try:
        query = f"SELECT * FROM lands WHERE id = {id}"
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return {
                "id": result[0],
                "field1": result[1],  # Replace with your actual column names
                "field2": result[2],
                # Add more fields as needed
            }
        else:
            return None
    except Exception as e:
        print(f"Query Error getting land service by id: {e}")

def delete_land_service_by_id(id):
    try:
        query = f"DELETE FROM lands WHERE id = {id}"
        cursor.execute(query)
        connection.commit()

        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Query Error deleting land service: {e}")

def update_land_service_by_id(id, land_data):
    try:
        query = "UPDATE lands SET landLocation = %s, soilType = %s, landArea = %s, cropType = %s, cultivationType = %s, cultivationHistory = %s, waterFacility = %s, landPrice = %s, landDesc = %s, landImage = %s, WHERE id = %s"
        values = (land_data['landLocation'], land_data['soilType'],land_data['landArea'],land_data['cropType'],land_data['cultivationType'],land_data['cultivationHistroy'],land_data['waterFacility'],land_data['landPrice'],land_data['landDesc'],land_data['landImage'], id)
        cursor.execute(query, values)
        connection.commit()
        if cursor.rowcount > 0:
            return True
        else:
            return False
    except Exception as e:
        print(f"Query Error updating land service: {e}")
