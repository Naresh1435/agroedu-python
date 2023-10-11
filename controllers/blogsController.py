from flask import   jsonify
from db.blogsQueries import get_all_blogs, create_blog, get_blog_by_id, delete_blog_by_id

def getBlogs(request):
    try:
        page = int(request.args.get('page', 1)) - 1
        limit = int(request.args.get('limit', 10))
        search = request.args.get('search', '')
        sort = request.args.get('sort', 'title')
        order = request.args.get('order', 'desc')

        blogs = get_all_blogs(page, limit, search, sort, order)  # Replace with your SQL query
        return jsonify(blogs)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error getting blogs', 'err': str(err)}), 500

def postBlog(request):
    try:
        user = request.json['user']
        title = request.json['title']
        content = request.json['content']
        tags = request.json['tags']

        blog_data = {
            'user': user,
            'title': title,
            'content': content,
            'tags': tags
        }

        result = create_blog(blog_data)  # Replace with your SQL query
        return jsonify(result)
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error creating blog', 'err': str(err)}), 500

def deleteBlog(id):
    try:
        blog = delete_blog_by_id(id)  # Replace with your SQL query

        if not blog:
            return jsonify({'msg': 'Blog not found'}), 404

        result = deleteBlogOnDb(id)  # Replace with your SQL query
        return jsonify({'result': result, 'msg': 'Blog deleted successfully'})
    except Exception as err:
        print(err)
        return jsonify({'msg': 'Error deleting blog', 'err': str(err)}), 500
