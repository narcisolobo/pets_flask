from os import environ
from flask import flash
from datetime import datetime
from dotenv import load_dotenv
from flask_app.models.user import User
from flask_app.config.mysql_connection import connectToMySQL


load_dotenv()


class Pet:
    _db = environ.get("DB_NAME")

    def __init__(self, data):
        self.id= int(data["id"])
        self.owner_id= int(data["owner_id"])
        self.owner = None
        self.type= data["type"]
        self.name = data["name"]
        self.is_derpy = data["is_derpy"]
        self.age= data["age"]
        self.created_at= data["created_at"]
        self.updated_at= data["updated_at"]

    def __repr__(self) -> str:
        return f"<Pet {self.name}>"

    @staticmethod
    def pet_is_valid(form_data):
        is_valid = True
        if len(form_data["type"].strip()) == 0:
            flash("Type is required.", "type")
            is_valid = False
        if len(form_data["name"].strip()) == 0:
            flash("Name is required.", "name")
            is_valid = False
        if len(form_data["age"].strip()) == 0:
            flash("Age is required.", "age")
            is_valid = False
        else:
            if not int(form_data["age"]) > 0:
                flash("Age must be greater than zero.", "age")
                is_valid = False
        return is_valid

    @classmethod
    def create_pet(cls, form_data):
        query = "INSERT INTO pets (owner_id, type, name, is_derpy, age) VALUES (%(owner_id)s, %(type)s, %(name)s, %(is_derpy)s, %(age)s);"
        return connectToMySQL(Pet._db).query_db(query, form_data)

    @classmethod
    def find_all_pets(cls):
        query = "SELECT * from pets JOIN users ON pets.owner_id = users.id;"
        results = connectToMySQL(Pet._db).query_db(query)
        pets = []
        for result in results:
            owner = User.find_user_by_id(result["owner_id"])
            pet = Pet(result)
            pet.owner = owner
            pets.append(pet)
        return pets

    @classmethod
    def find_one_pet(cls, pet_id: int):
        query = "SELECT * from pets WHERE id = %(pet_id)s;"
        data = {
            "pet_id": pet_id
        }
        results = connectToMySQL(Pet._db).query_db(query, data)
        if len(results) > 0:
            owner = User.find_user_by_id(results[0]["owner_id"])
            pet = Pet(results[0])
            pet.owner = owner
            return pet
        return None

    @classmethod
    def update_one_pet(cls, form_data):
        query = "UPDATE pets SET type = %(type)s, name = %(name)s, is_derpy = %(is_derpy)s, age = %(age)s  WHERE id = %(pet_id)s;"
        return connectToMySQL(Pet._db).query_db(query, form_data)

    @classmethod
    def delete_one_pet(cls, pet_id: int):
        query = "DELETE from pets WHERE id = %(pet_id)s;"
        data = {
            "pet_id": pet_id
        }
        return connectToMySQL(Pet._db).query_db(query, data)
