from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
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