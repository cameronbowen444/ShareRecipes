from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import recipe
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "real_recipes"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    @staticmethod
    def validate_user(user):
        is_valid = True

        email = user.get('email', '').strip()
        first_name = user.get('first_name', '').strip()
        last_name = user.get('last_name', '').strip()
        password = user.get('password', '')
        confirm = user.get('confirm', '')

        if not email:
            flash("Email is required!", "register")
            is_valid = False
        elif not EMAIL_REGEX.match(email):
            flash("Invalid email format!", "register")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(User.db).query_db(query, {"email": email})

            if results is False:
                flash("Database error. Please try again.", "register")
                return False

            if len(results) >= 1:
                flash("Email already in use!", "register")
                is_valid = False

        if len(first_name) < 3:
            flash("First name must be at least 3 characters!", "register")
            is_valid = False

        if len(last_name) < 3:
            flash("Last name must be at least 3 characters!", "register")
            is_valid = False

        if len(password) < 8:
            flash("Password must be at least 8 characters!", "register")
            is_valid = False

        if confirm != password:
            flash("Passwords do not match!", "register")
            is_valid = False

        return is_valid



    @classmethod 
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod 
    def get_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        
        if len(results) < 1:
            return False
        return cls(results[0])


    @classmethod 
    def get_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        if len(results) < 1:
            return False

        return cls(results[0])