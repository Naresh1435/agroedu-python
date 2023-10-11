import mysql.connector
from config.sql_connect import connect_mysql

connection = connect_mysql()
cursor = connection.cursor()

def find_user(email):
    query = f"SELECT * FROM users WHERE email = '{email}'"
    cursor.execute(query)
    user = cursor.fetchone()
    return user

def get_all_users(page, limit, search, sort, order):
    offset = page * limit
    query = f"SELECT * FROM users WHERE name LIKE '%{search}%' OR email LIKE '%{search}%' ORDER BY {sort} {order} LIMIT {limit} OFFSET {offset}"
    cursor.execute(query)
    users = cursor.fetchall()

    total_query = f"SELECT COUNT(*) FROM users WHERE name LIKE '%{search}%' OR email LIKE '%{search}%'"
    cursor.execute(total_query)
    total = cursor.fetchone()[0]

    total_pages = total / limit
    return {'page': page + 1, 'user': users, 'total': total, 'totalPages': total_pages}

def create_new_user(userData):
    query = f"INSERT INTO users (name, email, uid, photoURL, mobile, date, userType) VALUES ('{userData['name']}', '{userData['email']}', {userData['uid']}, {userData['photoURL']}, {userData['mobile']}, {userData['date']}, {userData['userType']})"
    cursor.execute(query)
   
    return userData

def update_user(id, userData):
    query = f"UPDATE users SET name = '{userData['name']}', email = '{userData['email']}',  WHERE id = {id}"
    cursor.execute(query)
    
    return userData

def delete_user(id):
    query = f"DELETE FROM users WHERE id = {id}"
    cursor.execute(query)
    
    return cursor.rowcount


def get_user_lands(id, page, limit, sort, order):
    try:
        offset = page * limit
        query = f"SELECT * FROM lands WHERE user = {id} ORDER BY {sort} {order} LIMIT {limit} OFFSET {offset};"
        cursor.execute(query)
        lands = cursor.fetchall()

        total_query = f"SELECT COUNT(*) FROM lands WHERE user = {id};"
        cursor.execute(total_query)
        total = cursor.fetchone()[0]

        total_pages = total // limit if total % limit == 0 else (total // limit) + 1

        return ({
            'page': page + 1,
            'lands': lands,
            'total': total,
            'totalPages': total_pages
        })

    except Exception as e:
        print("Error getting user lands:", str(e))
        raise e
    finally:
        cursor.close()



