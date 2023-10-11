from flask import Flask, request, send_from_directory, jsonify
from flask_cors import CORS
from functools import wraps
import jwt
import os



from flask_uploads import UploadSet, configure_uploads, IMAGES, UploadNotAllowed


from controllers.userController import (
    getUsers, postUsers, updateUsers, updateUserByAdmin, deleteUserByAdmin,
    getUserLands, getUserProducts
)
from controllers.landServiceController import (
    getAllLandServices, getLandServicesInCategory,createLandServiceRoute, deleteLandService, getLandServiceById, updateLandService
)
from controllers.productController import getProducts, getProductById, postProduct, deleteProduct
from controllers.donationController import postDonation, getDonations
from controllers.galleryController import getGallery, postGallery, deleteGallery
from controllers.blogsController import getBlogs, postBlog, deleteBlog




app = Flask(__name__)
CORS(app)

lands = UploadSet("lands", IMAGES)
products = UploadSet("products", IMAGES)
gallery = UploadSet("gallery", IMAGES)
app.config["UPLOADED_LANDS_DEST"] = "uploads/lands"  # Folder for land images
app.config["UPLOADED_PRODUCTS_DEST"] = "uploads/products"  # Folder for product images
app.config["UPLOADED_GALLERY_DEST"] = "uploads/gallery"

app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET')


configure_uploads(app, lands)
configure_uploads(app, products)
configure_uploads(app, gallery)

app.use_json = True







# Define routes




def upload_decorator(upload_set):
    def decorator(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            if 'file' in request.files:
                try:
                    uploaded_file = request.files['file']
                    if uploaded_file:
                        filename = uploaded_file.filename
                        upload_set.save(uploaded_file,name=uploaded_file.filename)
                        request.file_name = filename
                        return view_func(*args, **kwargs)
                except UploadNotAllowed:
                    return 'File type not allowed', 400
            return 'No file provided or wrong request method', 400

        return decorated_view
    return decorator
def multiple_file_upload(upload_set):
    def decorator(view_func):
        @wraps(view_func)
        def decorated_view(*args, **kwargs):
            if 'files' in request.files:
                try:
                    uploaded_files = request.files.getlist('files')
                    filenames = []
                    for uploaded_file in uploaded_files:
                        if uploaded_file:
                            filename = uploaded_file.filename
                            upload_set.save(uploaded_file, name=filename)
                            filenames.append(filename)
                    request.file_names = filenames
                    return view_func(*args, **kwargs)
                except UploadNotAllowed:
                    return 'One or more file types are not allowed', 400
            return 'No files provided or wrong request method', 400

        return decorated_view

    return decorator

def auth_middleware(required_role=None):
    def decorator(next_middleware):
        @wraps(next_middleware)
        def wrapper(*args, **kwargs):
            token = request.headers.get('auth-token')

            if not token:
                return jsonify({'msg': 'Authorization denied'}), 401

            try:
                decoded = jwt.decode(token, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
                if required_role and decoded.get('role') != required_role:
                    return jsonify({'msg': 'Authorization denied'}), 401

                kwargs['user'] = decoded
                return next_middleware(*args, **kwargs)
            except jwt.ExpiredSignatureError:
                return jsonify({'msg': 'Token Expired'}), 401
            except jwt.InvalidTokenError:
                return jsonify({'msg': 'Token Invalid'}), 401

        return wrapper

    return decorator

def auth():
    return auth_middleware()

def adminAuth():
    return auth_middleware(required_role='admin')

@app.route("/api/postDonation", methods=["POST"])
def create_donation():
    return postDonation(request)

@app.route("/api/getDonations", methods=["GET"])
def get_all_donations():
    return getDonations(request)

@app.route("/api/postGallery", methods=["POST"])
@adminAuth()
@upload_decorator(gallery)
def create_gallery():
    return postGallery(request)

@app.route("/api/getGallery", methods=["GET"])
def get_all_gallery():
    return getGallery(request)

@app.route("/api/deleteGallery/<int:id>", methods=["DELETE"])
@adminAuth()
def delete_gallery(id):
    return deleteGallery(id)

@app.route("/api/getUser", methods=["GET"])
@adminAuth()
def get_all_users():
    return getUsers(request)

@app.route("/api/postUser", methods=["POST"])
def create_user():
    return postUsers(request)

@app.route("/api/updateUser", methods=["PUT"])
@auth()
def update_user():
    return updateUsers(request)

@app.route("/api/updateUser/<int:id>", methods=["PUT"])
@adminAuth()
def update_user_by_admin(id):
    return updateUserByAdmin(request, id)

@app.route("/api/deleteUser/<int:id>", methods=["DELETE"])
@adminAuth()
def delete_user_by_admin(id):
    return deleteUserByAdmin(request, id)

@app.route("/api/userLands/<int:id>", methods=["GET"])
@auth()
def get_user_lands(id):
    return getUserLands(request, id)

@app.route("/api/userProducts/<int:id>", methods=["GET"])
@auth()
def get_user_products(id):
    return getUserProducts(request, id)

@app.route("/api/getLandService", methods=["GET"])
@auth()
def get_all_land_services():
    return getAllLandServices(request)

@app.route("/api/getLandService/<int:id>", methods=["GET"])
@auth()
def get_land_service_by_id(id):
    return getLandServiceById(request, id)

@app.route("/api/postLandService", methods=["POST"])
@auth()
@multiple_file_upload(lands)
def create_land_service():
    return createLandServiceRoute(request)

@app.route("/api/updateLandService/:id", methods=["PUT"])
@auth()
@multiple_file_upload(lands)
def update_land_service():
    return updateLandService(request,id)


@app.route("/api/deleteLandService/<int:id>", methods=["DELETE"])
@auth()
def delete_land_service(id):
    return deleteLandService(request, id)

@app.route("/api/getProduct", methods=["GET"])
@auth()
def get_all_products():
    return getProducts(request)

@app.route("/api/getProduct/<int:id>", methods=["GET"])
@auth()
def get_product_by_id(id):
    return getProductById(request, id)

@app.route("/api/postProduct", methods=["POST"])
@auth()
@multiple_file_upload(products)
def create_product():
    return postProduct(request)

@app.route("/api/deleteProduct/<int:id>", methods=["DELETE"])
@auth()
def delete_product(id):
    return deleteProduct(request, id)

@app.route("/api/getBlogs", methods=["GET"])
def get_all_blogs():
    return getBlogs(request)

@app.route("/api/postBlog", methods=["POST"])
@adminAuth()
def create_blog():
    return postBlog(request)

@app.route("/api/deleteBlog/<int:id>", methods=["DELETE"])
@adminAuth()
def delete_blog(id):
    return deleteBlog(request, id)

@app.route('/uploads/<folder>/<filename>')
def serve_file(folder, filename):
    base_directory = os.path.join(os.getcwd(), 'uploads', folder)
    return send_from_directory(base_directory, filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 3000))
    app.run(debug=True, port=port)

