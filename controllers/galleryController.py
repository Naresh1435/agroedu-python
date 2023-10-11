from flask import jsonify
import os
from db.galleryQueries import create_gallery, get_all_gallery, delete_from_gallery

def postGallery(request):
    try:
        content = request.args.get('content', '')
        image = 'uploads/gallery' + request.file_name
        
        gallery_data = {
            'content': content,
            'image': image
        }
        result = create_gallery(gallery_data)
        return jsonify(result)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error posting gallery', 'err': str(err)}), 500
def getGallery():
    try:
        gallery = get_all_gallery()
        return jsonify(gallery)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting gallery', 'err': str(err)}), 500
def deleteGallery(id):
    try:
        gallery = delete_from_gallery(id)
        if not gallery:
            return jsonify({'msg': 'Gallery not found'}), 404
        os.remove(os.path.join('uploads', 'gallery', gallery['image']))
        return jsonify({'gallery': gallery, 'msg': 'Gallery deleted successfully'})
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error deleting gallery', 'err': str(err)}), 500