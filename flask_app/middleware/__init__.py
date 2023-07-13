from functools import wraps
from flask_app.models.user import User
from flask import flash, g, redirect, session, url_for


def login_required(f):
    """ Route guard and global user provider. """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Please log in.", "auth")
            return redirect(url_for('login'))
        user = User.find_user_by_id(session["user_id"])
        g.user = user
        return f(*args, **kwargs)

    return decorated_function
