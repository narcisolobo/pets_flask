from flask_app import app

# remember to import controllers!!
from flask_app.controllers import users, pets

if __name__ == "__main__":
    app.run(host="localhost", port=5001, debug=True)