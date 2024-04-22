from config import app, api
from models import Post, Comment
from flask_restful import Resource

class SortedPosts(Resource):
  def get(self):
    posts = Post.query.order_by(Post.title.asc()).all()
    return [post.to_dict() for post in posts]
  
class PostsByAuthor(Resource):
  def get(self, author):
    posts = Post.query.filter_by(author=author).all()
    return [post.to_dict() for post in posts]
  
class PostsByTitle(Resource):
  def get(self, title):
    posts = Post.query.all()
    return [post.to_dict() for post in posts if title.lower() in post.title.lower()]
  
class SortPostsByComments(Resource):
  def get(self):
    posts = Post.query.all()
    posts.sort(reverse=True, key=lambda post: len(post.comments))
    return [post.to_dict() for post in posts]
    # the sort() method will return None if you save it in a variable, it makes an in-place sorting
  
api.add_resource(SortedPosts, '/api/sorted_posts')
api.add_resource(PostsByAuthor, '/api/posts_by_author/<string:author>')
api.add_resource(PostsByTitle, '/api/search_posts/<string:title>')
api.add_resource(SortPostsByComments, '/api/posts_ordered_by_comments')

if __name__ == "__main__":
  app.run(port=5555, debug=True)