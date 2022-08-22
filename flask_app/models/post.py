from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user import User
db = 'forums'

class Post:
    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.post = data['post']
        self.topic = data['topic']
        self.users_id = data['users_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = None
        self.users_who_liked = []
        self.user_ids_who_liked = []

    @classmethod
    def add_post(cls, data):
        query = 'INSERT INTO posts (title, post, topic, users_id) VALUES (%(title)s, %(post)s, %(topic)s, %(users_id)s);'
        return connectToMySQL(db).query_db(query, data)


    @classmethod
    def get_post_by_id(cls, data):
        query = 'SELECT * FROM posts WHERE id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def get_by_topic(cls, data):
        query = 'SELECT * FROM posts ORDER BY desc WHERE topic = %(topic)s;'
        results = connectToMySQL(db).query_db(query, data)
        post_list = []
        for each_post in results:
            post_obj = cls(each_post)
            post_list.append(post_obj)
        return post_list

    # get all posts (one to many)
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON posts.users_id=users.id;"
        results = connectToMySQL(db).query_db(query)
        posts = []
        for row in results:
            post = cls(row)
            #create associated user (author) object
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = User(user_data)
            post.user = user
            posts.append(post)
        return posts

    @classmethod
    def delete_post(cls, data):
        query = 'DELETE FROM posts WHERE id = %(id)s'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_all_posts_desc(cls):
        query = "SELECT * FROM posts JOIN users ON posts.users_id=users.id ORDER BY posts.created_at DESC;"
        results = connectToMySQL(db).query_db(query)
        posts = []
        for row in results:
            post = cls(row)
            #create associated user (author) object
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            user = User(user_data)
            post.user = user
            posts.append(post)
        return posts


    @classmethod
    def get_one_post(cls, data):
        query = "SELECT * FROM posts JOIN users ON posts.users_id=users.id WHERE posts.id=%(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        row = results[0]
        post = cls(row)
        user_data = {
            'id': row['users.id'],
            'first_name': row['first_name'],
            'last_name': row['last_name'],
            'email': row['email'],
            'password': row['password'],
            'created_at': row['users.created_at'],
            'updated_at': row['users.updated_at']
        }
        user = User(user_data)
        post.user = user
        return post



    @staticmethod
    def validate_post_form(post):
        is_valid = True
        if len(post["title"]) < 1:
            flash("Title must be at least 1 character.")
            is_valid = False
        if len(post["post"]) < 10:
            flash("Content must be at least 10 characters.")
            is_valid = False
        return is_valid



class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts_id = data['posts_id']
        self.users_id = data['users_id']
        self.author = None

    @classmethod
    def get_comments(cls, data):
        query = 'SELECT * FROM comments JOIN users ON comments.users_id = users.id  WHERE posts_id = %(id)s;'
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        comment_list = []
        for each_comment in results:
            comment_obj = cls(each_comment)
            comment_list.append(comment_obj)
            user_data ={
                'id': each_comment['users.id'],
                'first_name': each_comment['first_name'],
                'last_name': each_comment['last_name'],
                'email': each_comment['email'],
                'password': each_comment['password'],
                'created_at': each_comment['users.created_at'],
                'updated_at': each_comment['users.updated_at']
            }
            comment_obj.author= User(user_data)
        return comment_list

    @classmethod
    def create_comment(cls, data):
        query = 'INSERT INTO comments (comment, users_id, posts_id) VALUES (%(comment)s, %(users_id)s, %(posts_id)s);'
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def delete_comment(cls, data):
        query = 'DELETE FROM comments WHERE id = %(id)s;'
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_comment(comment):
        valid = True
        if len(comment) == 0:
            flash('Comment cannot be empty.')
            valid = False
        if len(comment) > 128:
            flash('Comment must be less than 128 characters.')
            valid = False
        return valid
