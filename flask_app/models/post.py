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
