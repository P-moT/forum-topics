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

    # get all posts (one to many) - Not sure if this works
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN users ON posts.user_id=users.id;"
        results = connectToMySQL(cls.db).query_db(query)
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


class Comment:
    def __init__(self, data):
        self.id = data['id']
        self.comment = data['comment']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts_id = data['posts_id']
        self.users_id = data['users_id']
        self.author = User(data)

    @classmethod
    def get_comments(cls, data):
        query = 'SELECT * FROM comments JOIN users ON comments.users_id = users.id  WHERE posts_id = %(posts_id)s;'
        results = connectToMySQL(db).query_db(query, data)
        print(results)
        comment_list = []
        for each_comment in results:
            comment_obj = cls(each_comment)
            comment_list.append(comment_obj)
        return comment_list

    @classmethod
    def create_comment(cls, data):
        query = 'INSERT INTO comments (comment, users_id, posts_id) VALUES (%(comment)s, %(users_id)s, %(posts_id)s);'
        return connectToMySQL(db).query_db(query, data)
