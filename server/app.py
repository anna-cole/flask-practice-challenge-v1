from config import app, api
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func

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
  
class SortPostsByComments(Resource):
  def get(self):
    posts = Post.query.outerjoin(Post.comments).group_by(Post.id).order_by(func.count().desc()).all()
    return [post.to_dict() for post in posts], 200

class MostPopularCommenter(Resource):
  def get(self):
    commenter_counts = Comment.query.with_entities(Comment.commenter, func.count(Comment.commenter)).group_by(Comment.commenter).all() # list of tuples, where each tuple contains the commenter's name and the count of their comments.
    most_popular_commenter = max(commenter_counts, key=lambda x: x[1])[0] # finds the tuple with the highest count by using the key argument with a lambda function that extracts the count from each tuple.[0] retrieves the commenter's name from the tuple with the highest count.
    return {"commenter": most_popular_commenter}, 200

api.add_resource(Posts, '/api/sorted_posts')
api.add_resource(PostsByAuthor, '/api/posts_by_author/<string:author>')
api.add_resource(PostsByTitle, '/api/search_posts/<string:title>')
api.add_resource(SortPostsByComments, '/api/posts_ordered_by_comments')
api.add_resource(MostPopularCommenter, '/api/most_popular_commenter')

if __name__ == "__main__":
  app.run(port=5555, debug=True)