import mysql.connector
from config.sql_connect import connect_mysql

# SQL query to create a blog
create_blog_query = """
INSERT INTO blogs (title, content, user_id)
VALUES (%s, %s, %s)
"""

# SQL query to get all blogs with pagination and search
get_all_blogs_query = """
SELECT *
FROM blogs
WHERE title LIKE %s
ORDER BY {sort} {order}
LIMIT %s OFFSET %s
"""

# SQL query to get a blog by ID
get_blog_by_id_query = """
SELECT *
FROM blogs
WHERE id = %s
"""

# SQL query to delete a blog by ID
delete_blog_by_id_query = """
DELETE FROM blogs
WHERE id = %s
"""


def create_blog(blog_data):
    connection = connect_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(create_blog_query, (blog_data['title'], blog_data['content'], blog_data['user_id']))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print("Error creating blog:", err)
            return False

def get_all_blogs(page, limit, search, sort, order):
    connection = connect_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            offset = page * limit
            cursor.execute(get_all_blogs_query.format(sort=sort, order=order), (f"%{search}%", limit, offset))
            blogs = cursor.fetchall()

            # Calculate total and totalPages (not included in MySQL result)
            cursor.execute("SELECT COUNT(*) FROM blogs WHERE title LIKE %s", (f"%{search}%",))
            total = cursor.fetchone()[0]
            total_pages = (total + limit - 1) // limit

            cursor.close()
            connection.close()
            return {
                "page": page + 1,
                "blogs": blogs,
                "total": total,
                "totalPages": total_pages,
            }
        except mysql.connector.Error as err:
            print("Error getting blogs:", err)
            return None

def get_blog_by_id(blog_id):
    connection = connect_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(get_blog_by_id_query, (blog_id,))
            blog = cursor.fetchone()
            cursor.close()
            connection.close()
            return blog
        except mysql.connector.Error as err:
            print("Error getting blog by ID:", err)
            return None

def delete_blog_by_id(blog_id):
    connection = connect_mysql()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(delete_blog_by_id_query, (blog_id,))
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except mysql.connector.Error as err:
            print("Error deleting blog:", err)
            return False
