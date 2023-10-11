from flask import jsonify
from db.productQueries import get_all_products, get_all_products_in_category, get_product_by_id, delete_product_by_id,create_product

def getProducts(request):
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')

        products = get_all_products(page, limit, search, sort, order)
        return jsonify(products)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting products', 'err': str(err)}), 500

def getProductsInCategory(request,category):
    try:
        page = int(request.args.get('page', 0))
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'date')
        order = request.args.get('order', 'desc')

        products = get_all_products_in_category(page, limit, search, sort, order, category)
        return jsonify(products)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting product category', 'err': str(err)}), 500

def postProduct(request):
    try:
        data = request.json
        productData = {
            "productName": data["productName"],
            "productCategory": data["productCategory"],
            "productManufacturer": data["productManufacturer"],
            "productDescription": data["productDescription"],
            "productPrice": data["productPrice"],
            "productQuantity": data["productQuantity"],
        }
        user = request.user.id
        productImage = ["uploads/products" + filename for filename in request.file_names]
        productData["user"] = user
        productData["productImage"] = ",".join(productImage)

        result = create_product(productData)
        return jsonify(result)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error creating product', 'err': str(err)}), 500
def getProductById(id):
    try:
        result = get_product_by_id(id)
        if not result:
            return jsonify({'msg': 'Product not found'}), 404
        return jsonify(result)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting product', 'err': str(err)}), 500
def deleteProduct(request,id):
    try:
        reqUser = request.user.id
        role = request.user.role
        doc = get_product_by_id(id)
        if not doc:
            return jsonify({'msg': 'Product not found'}), 404
        docUser = str(doc.user["_id"])
        if reqUser != docUser and role != "admin":
            return jsonify({'msg': 'Unauthorized'}), 401
        result = delete_product_by_id(id)
        photos = result.get("productImage", [])
        for photo in photos:
            # Add code to delete the photos from the server
            pass
        return jsonify({'result': result, 'msg': 'Product deleted successfully'})
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error deleting product', 'err': str(err)}), 500
