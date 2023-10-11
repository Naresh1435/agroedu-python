from flask import jsonify, abort
import os
from db.landServiceQueries import get_all_land_services, get_all_land_services_in_category, get_land_service_by_id, delete_land_service_by_id, update_land_service_by_id, create_land_service
def getAllLandServices(request):
    try:
        # Parse query parameters
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'landLocation')
        order = request.args.get('order', 'desc')

        land_services = get_all_land_services(page, limit, search, sort, order)
        return jsonify(land_services)
    except Exception as e:
        return jsonify({"msg": "Error getting lands", "err": str(e)}), 500
    
def getLandServicesInCategory(request, category):
    try:
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')
        land_services = get_all_land_services_in_category(page, limit, search, sort, order, category)
        return jsonify(land_services)
    except Exception as e:
        return jsonify({"msg": "Error getting land category", "err": str(e)}), 500

def createLandServiceRoute(request):
    try:
        user = request.json['user']
        land_location = request.json['landLocation']
        soil_type = request.json['soilType']
        land_area = request.json['landArea']
        crop_type = request.json['cropType']
        cultivation_type = request.json['cultivationType']
        cultivation_history = request.json['cultivationHistory']
        water_facility = request.json['waterFacility']
        land_price = request.json['landPrice']
        land_desc = request.json['landDesc']
        land_images = ['uploads/lands'+file_name for file_name in request.file_names]
        land_image = ",".join(land_images)
        land_data = {
            "user": user,
            "landLocation": land_location,
            "soilType": soil_type,
            "landArea": land_area,
            "cropType": crop_type,
            "cultivationType": cultivation_type,
            "cultivationHistory": cultivation_history,
            "waterFacility": water_facility,
            "landPrice": land_price,
            "landDesc": land_desc,
            "landImage": land_image
        }

        result = create_land_service(land_data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"msg": "Error creating land", "err": str(e)}), 500

def getLandServiceById(id):
    try:
        result = get_land_service_by_id(id)
        if not result:
            return jsonify({"msg": "Land not found"}), 404
        return jsonify(result)
    except Exception as e:
        return jsonify({"msg": "Error getting land", "err": str(e)}), 500
    
def deleteLandService(request,id):
    try:
        req_user = request.json['user']
        role = request.json['role']
        doc = get_land_service_by_id(id)
        if not doc:
            return jsonify({"msg": "Land not found"}), 404
        doc_user = doc['user']
        if req_user != doc_user and role != "admin":
            return jsonify({"msg": "Unauthorized"}), 401
        result = delete_land_service_by_id(id)
        photos = doc['landImage']
        for photo in photos:
            os.remove(photo)
        return jsonify({"result": result, "msg": "Land deleted successfully"})
    except Exception as e:
        return jsonify({"msg": "Error deleting land", "err": str(e)}), 500

def updateLandService(request,id):
    try:
        req_user = request.json['user']
        role = request.json['role']
        doc = get_land_service_by_id(id)
        if not doc:
            return jsonify({"msg": "Land not found"}), 404
        doc_user = doc['user']
        if req_user != doc_user and role != "admin":
            return jsonify({"msg": "Unauthorized"}), 401

        land_location = request.json.get('landLocation')
        soil_type = request.json.get('soilType')
        land_area = request.json.get('landArea')
        crop_type = request.json.get('cropType')
        cultivation_type = request.json.get('cultivationType')
        cultivation_history = request.json.get('cultivationHistory')
        water_facility = request.json.get('waterFacility')
        land_price = request.json.get('landPrice')
        land_desc = request.json.get('landDesc')
        land_image = request.json.get('landImage')

        land_data = {
            "landLocation": land_location,
            "soilType": soil_type,
            "landArea": land_area,
            "cropType": crop_type,
            "cultivationType": cultivation_type,
            "cultivationHistory": cultivation_history,
            "waterFacility": water_facility,
            "landPrice": land_price,
            "landDesc": land_desc,
            "landImage": land_image
        }

        result = update_land_service(id, land_data)
        return jsonify({"result": result, "msg": "Land updated successfully"})
    except Exception as e:
        return jsonify({"msg": "Error updating land", "err": str(e)}), 500
