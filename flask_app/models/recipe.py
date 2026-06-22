from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash
import re

class Recipe:
    db = "real_recipes"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date = data['date']
        self.under30 = data['under30']
        self.user_recipe = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None

    @staticmethod
    def validate_recipe(recipe):
        is_valid = True
        if len(recipe['name']) < 3:
            flash('Recipe name must be at least 3 characters', 'recipe')
            is_valid = False
        if len(recipe['description']) < 3:
            flash('Description must be at least 3 characters', 'recipe')
            is_valid = False
        if len(recipe['instructions']) < 3:
            flash('Instructions must be at least 3 characters', 'recipe')
            is_valid = False
        if recipe['date'] == '':
            flash('Date is required', 'recipe')
            is_valid = False
        return is_valid



    @classmethod
    def save_recipe(cls, data):
        query = "INSERT INTO recipes (name, description, instructions, date, under30, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(date)s, %(under30)s, %(user_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit_recipe(cls, data):
        query = """
        UPDATE recipes
        SET 
            name = %(name)s,
            description = %(description)s,
            instructions = %(instructions)s,
            date = %(date)s,
            under30 = %(under30)s,
            updated_at = NOW()
        WHERE id = %(id)s;
        """
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete_recipe(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_recipe_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod 
    def get_recipes(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        all_recipes = []
        for row in results:
            all_recipes.append(cls(row))
        return all_recipes