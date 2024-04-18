from config import app, api
from models import Post, Comment
from flask_restful import Resource
from sqlalchemy import func

# This route should return as json all the posts alphabetized by title. Flask RESTful does the json for you, so no need to use jsonify. To sort a list, use the sort() method. This method only works with iterables, like lists. It is a destructive method, but it's ok to use here as it will only modify the list within this function. The default of sort() is ascending order.
class PostsSortedByTitle(Resource):
  def get(self):
    # posts = Post.query.order_by(Post.title.asc()).all()
    # return [post.to_dict() for post in posts], 200
    posts = Post.query.all()
    posts.sort(key=lambda post: post.title) # post.title are strings
    return [post.to_dict() for post in posts], 200

# This route should return as json the post by the author's name.  
class PostsFilteredByAuthor(Resource):
  def get(self, author):
    # posts = Post.query.all()
    # return [post.to_dict() for post in posts if post.author.lower() == author.lower()], 200
    posts = Post.query.filter_by(author=author).all()
    return [post.to_dict() for post in posts], 200

# This route should return as json all the posts that include the title. Capitalization shouldn't matter. Search by word in title.
class PostsSearchByTitle(Resource):
  def get(self, title):
    # posts = Post.query.all() # list of objects
    # title_words = title.lower().split() # ['frog']
    # return [post.to_dict() for post in posts if any(word in post.title.lower() for word in title_words)], 200
    posts = Post.query.all()
    return [post.to_dict() for post in posts if title.lower() in post.title.lower()], 200

# This route should return as json the posts ordered by how many comments the post has, in descending order. Descending order means you will have to sort the posts by the number of its comments. Comments is a relationship of the Post model. It's a list of all the comments that a post has. You sort lists with the sort() method. Use the lambda function to establish the sorting criteria. Use the reverse parameter for descending. To get the number of comments out of the list, use the len() method. 
class PostsSortedByComments(Resource):
  def get(self):
    # posts = Post.query.outerjoin(Post.comments).group_by(Post.id).order_by(func.count().desc()).all()
    # return [post.to_dict() for post in posts], 200
    posts = Post.query.all()
    posts.sort(reverse=True, key=lambda post: len(post.comments)) # post.comments is a list of objects. len(post.comments) is the criteria for the sorting method. 
    return [post.to_dict() for post in posts] 

# This route should return as json a dictionary like { commenter: "Bob" } of the commenter that's made the most comments. Commenter is an attribute of the Comment model, so no need to get anything from the Post model. You will have to keep track of each commenter and the count of their comments. 
class MostPopularCommenter(Resource):
  def get(self):
    # commenter_counts = Comment.query.with_entities(Comment.commenter, func.count(Comment.commenter)).group_by(Comment.commenter).all() # list of tuples, where each tuple contains the commenter's name and the count of their comments.
    # most_popular_commenter = max(commenter_counts, key=lambda x: x[1])[0] # finds the tuple with the highest count by using the key argument with a lambda function that extracts the count from each tuple.[0] retrieves the commenter's name from the tuple with the highest count.
    # return {"commenter": most_popular_commenter}, 200
    
    comments = Comment.query.all()
    
    commenters = []
    
    for comment in comments:
      commenters.append(comment.commenter) # will make a list with the commenters 

    dict_list = []
    
    for commenter in set(commenters): # will make a collection of unique commenters (set) 
      count = commenters.count(commenter) # count the number of times each commenter shows in the original list
      dict_list.append({commenter: count}) # will make a list of dicts {commenter: number}

    #print(dict_list) # [{'Frank': 2}, {'Sam': 3}, {'Sara': 1}]

    dict_list.sort(reverse=True, key=lambda dict: list(dict.values())[0]) # will sort the dicts in descending order by their values. The [0] will extract each value from its list [2][3][1] => 2, 3, 1. Then, the sort method will sort the dicts based on those numbers.

    return {'Commenter': list(dict_list[0].keys())[0]} # had to make a list to extract the key from the dict_keys object

api.add_resource(PostsSortedByTitle, '/api/sorted_posts')
api.add_resource(PostsFilteredByAuthor, '/api/posts_by_author/<string:author>')
api.add_resource(PostsSearchByTitle, '/api/search_posts/<string:title>')
api.add_resource(PostsSortedByComments, '/api/posts_ordered_by_comments')
api.add_resource(MostPopularCommenter, '/api/most_popular_commenter')

if __name__ == "__main__":
  app.run(port=5555, debug=True)