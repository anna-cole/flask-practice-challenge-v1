from config import app, api
from models import Post, Comment
from flask_restful import Resource
from flask import jsonify

# create routes here:

class Posts(Resource):
  def get(self):
    posts = Post.query.order_by(Post.title.asc()).all()
    return [post.to_dict() for post in posts], 200
  
class PostsByAuthor(Resource):
  def get(self, author):
    all_posts = Post.query.all()
    matching_posts = [post.to_dict() for post in all_posts if post.author.lower() == author.lower()]
    return matching_posts, 200
  
class PostsByTitle(Resource):
  def get(self, title):
    all_posts = Post.query.all() # list of objects
    title_words = title.lower().split() # ['frog']
    matching_posts = [post.to_dict() for post in all_posts if any(word in post.title.lower() for word in title_words)]
    return matching_posts, 200

api.add_resource(Posts, '/api/sorted_posts')
api.add_resource(PostsByAuthor, '/api/posts_by_author/<string:author>')
api.add_resource(PostsByTitle, '/api/search_posts/<string:title>')

if __name__ == "__main__":
  app.run(port=5555, debug=True)