from flask import flash
import re
from flask_app.config.mysqlconnection import connectToMySQL
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
db = 'forums'

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @staticmethod
    def validate_login(login_cred):
        valid = True
        if not EMAIL_REGEX.match(login_cred['email']):
            flash('Invalid email address.', 'login')
            valid = False
        if not login_cred['email']:
            flash ('Password cannot be empty', 'login')
            valid = False
        return valid
        

    @staticmethod
    def validate_user(user, data):
        valid = True
        query = "SELECT * FROM users WHERE email = %(email)s;"
        user_list = connectToMySQL(db).query_db(query, data)
        if len(user_list) > 0:
            flash('Email is already registered.', 'register')
            valid = False
        if len(user['first_name']) < 1:
            flash("First name must be at least 1 character.", 'register')
            valid = False 
        if len(user['last_name']) < 1:
            flash("Last name must be at least 1 character.", 'register')
            valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email address.', 'register')
            valid = False
        if len(user['password']) < 8:
            flash('Password must be at least 8 characters', 'register')
            valid = False
        if user['password'] != user['confirm_pw']:
            flash('Passwords do not match.', 'register')
            valid = False
        return valid
    
    # validation - update user profile
    @staticmethod
    def validate_user_update(user):
        is_valid = True
        if len(user["first_name"]) < 3:
            flash("First name must be at least 3 characters.")
            is_valid = False
        if len(user["last_name"]) < 3:
            flash("Last name must be at least 3 characters.")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!")
            is_valid = False
        return is_valid


    @classmethod
    def add_user(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(db).query_db(query, data)
    
    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s"
        user = connectToMySQL(db).query_db(query, data)
        return cls(user[0])

    @classmethod
    def grab_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s'
        result = connectToMySQL(db).query_db(query, data)
        if not result:
            return False
        return cls(result[0])
    
    # update user profile
    @classmethod
    def get_user_by_id(cls, data):
        query = "SELECT * FROM users WHERE id=%(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        #Check to see if there were any results, if not, the email does not exist in the db
        if len(results) < 1:
            return False
        row = results[0]
        user = cls(row)
        return user


    # update user profile
    @classmethod
    def update(cls, data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id=%(id)s;"
        return connectToMySQL(db).query_db(query, data)
