from flask import jsonify
import jwt
from dotenv import load_dotenv
import os
from db.userQueries import create_new_user, update_user, delete_user, get_all_users, find_user

SECRET_KEY = os.environ.get('JWT_SECRET')

def getUsers(request):
    try:
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')

        users = get_all_users(page, limit, search, sort, order)
        return jsonify(users)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting users', 'err': str(err)}), 500

def postUsers():
    data = request.json
    uid = data['uid']
    name = data['name']
    email = data['email']
    mobile = data['mobile']
    photoURL = data['photoURL']
    userType = data['userType']

    try:
        user = find_user(email)
        if user:
            payload = {
                'user': {
                    'id': user['id'],
                    'role': user['userType']
                }
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({'token': token, 'user': user})

        else:
            user = {
                'uid': uid,
                'name': name,
                'email': email,
                'mobile': mobile,
                'photoURL': photoURL,
                'userType': userType
            }

            user = create_new_user(user)
            payload = {
                'user': {
                    'id': user['id'],
                    'role': user['user_type']
                }
            }
            token = jwt.encode(payload, SECRET_KEY , algorithm='HS256')
            return jsonify({'token': token, 'user': user})

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error creating user', 'err': str(err)}), 500
def updateUsers(request):
    user_id = request.user['id']
    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    photoURL = data.get('photoURL')
    user_type = data.get('userType')

    try:
        user_data = {
            'name': name,
            'mobile': mobile,
            'photoURL': photoURL,
            'user_type': user_type
        }

        user = update_user(user_id, user_data)
        return jsonify(user)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error updating user', 'err': str(err)}), 500
def updateUserByAdmin(request,id):
    data = request.json
    name = data.get('name')
    mobile = data.get('mobile')
    photoURL = data.get('photoURL')
    user_type = data.get('userType')

    try:
        user_data = {
            'name': name,
            'mobile': mobile,
            'photoURL': photoURL,
            'user_type': user_type
        }

        user = update_user(id, user_data)
        return jsonify(user)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error updating user', 'err': str(err)}), 500
def deleteUserByAdmin(id):
    try:
        user = delete_user(id)
        if not user:
            return jsonify({'msg': 'User not found'}), 404
        return jsonify({'user': user, 'msg': 'User deleted'})

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error deleting user', 'err': str(err)}), 500
def getUserLands(request,id):
    try:
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        order = request.args.get('order', 'desc')
        sort = request.args.get('sort', 'updatedAt')

        response = get_user_lands(id, page, limit, sort, order)
        if not response:
            return jsonify({'msg': 'User not found'}), 404
        return jsonify(response)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting user lands', 'err': str(err)}), 500
def getUserProducts(request,id):
    try:
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        order = request.args.get('order', 'desc')
        sort = request.args.get('sort', 'updatedAt')

        response = get_user_products(id, page, limit, sort, order)
        if not response:
            return jsonify({'msg': 'User not found'}), 404
        return jsonify(response)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting user products', 'err': str(err)}), 500
