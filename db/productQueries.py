import mysql.connector
from config.sql_connect import connect_mysql

connection = connect_mysql()
cursor = connection.cursor()

def get_all_products(page, limit, search, sort, order):
    offset = page * limit
    query = """
        SELECT * FROM products
        WHERE productName LIKE %s
        ORDER BY {} {}
        LIMIT %s OFFSET %s
    """.format(sort, order)
    cursor.execute(query, ('%' + search + '%', limit, offset))
    products = cursor.fetchall()

    query = """
        SELECT COUNT(*) FROM products
        WHERE productName LIKE %s
    """
    cursor.execute(query, ('%' + search + '%',))
    total = cursor.fetchone()[0]
    total_pages = (total + limit - 1) // limit  # Calculate total pages

    return {
        "page": page + 1,
        "products": products,
        "total": total,
        "totalPages": total_pages,
    }

def get_all_products_in_category(page, limit, search, sort, order, category):
    offset = page * limit
    query = """
        SELECT * FROM products
        WHERE productName LIKE %s AND productCategory = %s
        ORDER BY {} {}
        LIMIT %s OFFSET %s
    """.format(sort, order)
    cursor.execute(query, ('%' + search + '%', category, limit, offset))
    products = cursor.fetchall()

    query = """
        SELECT COUNT(*) FROM products
        WHERE productName LIKE %s AND productCategory = %s
    """
    cursor.execute(query, ('%' + search + '%', category))
    total = cursor.fetchone()[0]
    total_pages = (total + limit - 1) // limit  # Calculate total pages

    return {
        "page": page + 1,
        "products": products,
        "total": total,
        "totalPages": total_pages,
    }

def create_product(product_data):
    query = """
        INSERT INTO products (user,productName,productCategory,productManufacturer,productDescription,productPrice,productQuantity, productImage)
        VALUES (%s, %s, %s,%s,%s, %s, %s,%s)
    """
    cursor.execute(query, (product_data['user'], product_data['productName'],product_data['productCategory'],product_data['productDescription'],product_data['productPrice'],product_data['productQuantity'],product_data['productImage'] ))
    connection.commit()
    return product_data

def get_product_by_id(id):
    query = """
        SELECT * FROM products
        WHERE id = %s
    """
    cursor.execute(query, (id,))
    product = cursor.fetchone()
    if not product:
        return None
    return product

def delete_product_by_id(id):
    query = """
        DELETE FROM products
        WHERE id = %s
    """
    cursor.execute(query, (id,))
    connection.commit()
    if cursor.rowcount == 0:
        return None
    return id
