from re import compile
from os import environ
from datetime import datetime
from flask import flash
from dotenv import load_dotenv
from flask_app.config.mysql_connection import connectToMySQL

EMAIL_REGEX = compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
PASSWORD_REGEX = compile(
    r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$")

load_dotenv()

class User:
    _db = environ.get("DB_NAME")

    def __init__(self, data: dict[str, str | datetime]) -> None:
        self.id: str = data["id"]
        self.first_name: str = data["first_name"]
        self.last_name: str = data["last_name"]
        self.email: str = data["email"]
        self.password: str = data["password"]
        self.created_at: datetime = data["created_at"]
        self.updated_at: datetime = data["updated_at"]

    def get_full_name(self):
        return f"<User {self.first_name} {self.last_name}>"

    @staticmethod
    def registration_is_valid(form_data: dict[str, str]) -> bool:
        is_valid = True
        if len(form_data["first_name"].strip()) < 2:
            flash("First name must be at least two characters.", "first_name")
            is_valid = False
        if len(form_data["last_name"].strip()) < 2:
            flash("Last name must be at least two characters.", "last_name")
            is_valid = False
        if len(form_data["email"].strip()) == 0:
            flash("Please enter your email address.", "email")
            is_valid = False
        else:
            if not EMAIL_REGEX.match(form_data["email"]):
                flash("Email is not valid.", "email")
                is_valid = False
        if len(form_data["password"].strip()) == 0:
            flash("Please enter your password.", "password")
            is_valid = False
        else:
            if not PASSWORD_REGEX.match(form_data["password"]):
                flash(
                    "At least 8 characters, 1 uppercase, 1 lowercase, 1 number.", "password")
                is_valid = False
            else:
                if form_data["confirm_password"] != form_data["password"]:
                    flash("Passwords do not match.", "confirm_password")
                    is_valid = False
        return is_valid

    @staticmethod
    def login_is_valid(form_data: dict[str, str]) -> bool:
        is_valid = True
        if len(form_data["email"].strip()) == 0:
            flash("Please enter your email address.", "email")
            is_valid = False
        else:
            if not EMAIL_REGEX.match(form_data["email"]):
                flash("Email is not valid.", "email")
                is_valid = False
        if len(form_data["password"].strip()) == 0:
            flash("Please enter your password.", "password")
            is_valid = False
        else:
            if not PASSWORD_REGEX.match(form_data["password"]):
                flash(
                    "At least 8 characters, 1 uppercase, 1 lowercase, 1 number.", "password")
                is_valid = False
        return is_valid

    @classmethod
    def register_user(cls, form_data: dict[str, str]) -> int:
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        return connectToMySQL(User._db).query_db(query, form_data)

    @classmethod
    def find_user_by_email(cls, email: str):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        data = {
            "email": email
        }
        results = connectToMySQL(User._db).query_db(query, data)
        if len(results) < 1:
            return False
        return User(results[0])

    @classmethod
    def find_user_by_id(cls, user_id: int):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        data = {
            "id": user_id
        }
        results = connectToMySQL(User._db).query_db(query, data)
        if len(results) < 1:
            return False
        return User(results[0])
