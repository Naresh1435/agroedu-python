from flask import jsonify
from db.donationQueries import create_donation, get_all_donations

def postDonation(request):
    try:
        data = request.json
        name = data.get('name')
        email = data.get('email')
        donation = data.get('donation')
        purpose = data.get('purpose')
        type = data.get('type')
        message = data.get('message')
        transaction_id = data.get('transactionId')
        transaction_mode = data.get('transactionMode')

        donate_data = {
            'name': name,
            'email': email,
            'donation': donation,
            'purpose': purpose,
            'type': type,
            'message': message,
            'transactionId': transaction_id,
            'transactionMode': transaction_mode,
        }

        result = create_donation(donate_data)
        return jsonify(result)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error posting donation', 'err': str(err)}), 500

def getDonations(request):
    try:
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'createdAt')
        order = request.args.get('order', 'desc')

        donations = get_all_donations(page, limit, search, sort, order)
        return jsonify(donations)

    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting donations', 'err': str(err)}), 500