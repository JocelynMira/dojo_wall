from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
import re

from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    
    DB= "dojo_wall"

    def __init__(self,data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.posts = []


    # CREATE
    @classmethod
    def save(cls, data):
        query = """INSERT INTO users (first_name, last_name, email, password)
                VALUES ( %(first_name)s, %(last_name)s, %(email)s, %(password)s)"""
        return connectToMySQL(cls.DB).query_db(query,data)

    # READ 
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM users"""
        users_from_db = connectToMySQL(cls.DB).query_db(query) 
        #results comes in a list of dictionaries
        users = []

        for user in users_from_db:
            users.append (cls (user) )
        return users

    @classmethod
    def get_user_by_id(cls, data):
        query = """SELECT * FROM users 
                WHERE id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query,data)
        return cls(results[0])
    
    @classmethod
    def get_user_by_email(cls, data):
        query = """SELECT * FROM users
                WHERE email = %(email)s """
        results = connectToMySQL(cls.DB).query_db(query,data)

        if len(results) < 1:
            return False
        return cls(results[0])
    

    # DELETE
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM users
                WHERE id = %(id)s
                """
        results = connectToMySQL(cls.DB).query_db(query, {'id': id })
        return results

    # REGISTER VALIDATIONS
    @staticmethod
    def validate_registration(user):
        is_valid = True
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL(User.DB).query_db(query, user)
        if len(results) >= 1:
            flash("Email already registered. Please log in!", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']):
            flash('Invalid email format!', "register")
            is_valid = False
        if len(user['first_name']) < 2:
            flash ('First Name must be at least 2 characters.', "register")
            is_valid = False
        if len(user['last_name']) < 2:
            flash ('Last Name must be at least 2 characters.', "register")
            is_valid = False
        if len(user['password']) < 8:
            flash ('Password must be at least 8 characters.', "register")
            is_valid = False
        if user['password'] != user['password2']:
            flash("Passwords do not match", "register")
            is_valid = False
        return is_valid



    # @classmethod
    # def get_dojo_with_ninjas(cls, data):
    #     query = """SELECT * FROM dojos
    #     LEFT JOIN ninjas ON ninjas.dojo_id = dojos.id
    #     WHERE dojos.id = %(id)s"""
    #     results = connectToMySQL(cls.DB).query_db(query, data)
    #     dojo = cls (results [0])
        
    #     for row_from_db in results:

    #         ninja_info = {
    #             "id" : row_from_db['ninjas.id'],
    #             "first_name": row_from_db['first_name'],
    #             "last_name": row_from_db['last_name'],
    #             "age": row_from_db['age'],
    #             "created_at": row_from_db['ninjas.created_at'],
    #             "updated_at": row_from_db['ninjas.updated_at']
    #         }
    #         dojo.ninjas.append( Ninja(ninja_info))
    #     return dojo