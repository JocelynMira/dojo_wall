from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import app
from flask_app.models.user_model import User


class Post:
    
    DB= "dojo_wall"

    def __init__(self,data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

    # CREATE
    @classmethod
    def save(cls, data):
        query = """INSERT INTO posts (content, user_id) VALUES ( %(content)s, %(user_id)s )"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return results

    # READ
    @classmethod
    def get_all(cls):
        query = """SELECT * FROM posts
                LEFT JOIN users ON posts.user_id = users.id
                """
        results = connectToMySQL(cls.DB).query_db(query)
        print(results)
        all_posts = []

        for post in results:
            one_post = cls(post)
            post_author = {
                'id': post['users.id'],
                'first_name': post['first_name'],
                'last_name': post['last_name'],
                'email': post['email'],
                'password': post['password'],
                'created_at': post['users.created_at'],
                'updated_at': post['users.updated_at'],
            }
            one_post.user = User(post_author)
            all_posts.append(one_post)
        return all_posts
    
    @classmethod
    def get_post_by_id(cls, data):
        query = """SELECT * FROM posts
                WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, data)
        return cls(results[0])

    # DELETE
    @classmethod
    def delete(cls, id):
        query = """DELETE FROM posts WHERE id = %(id)s;"""
        results = connectToMySQL(cls.DB).query_db(query, {'id': id})
        return results

    # POST VALIDATIONS
    @staticmethod
    def validate_posts(post):
        is_valid = True
        if len(post['content']) < 1:
            flash ('* Post content cannot be blank', "post")
            is_valid = False
        return is_valid