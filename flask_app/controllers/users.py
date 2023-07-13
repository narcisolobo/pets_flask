from flask_app import app
from flask_app.models.user import User
from flask_app import bcrypt
from flask import (
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        if not User.registration_is_valid(request.form):
            return redirect(url_for('register'))

        user = User.find_user_by_email(request.form['email'])
        if user:
            flash('Email in use. Please login.', 'auth')
            return redirect(url_for('login'))

        pw_hash = bcrypt.generate_password_hash(request.form['password'])
        data = {
            "first_name": request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
            "password": pw_hash,
        }

        user_id = User.register_user(data)
        session['user_id'] = user_id

        return redirect(url_for('all_pets'))
    return render_template("/users/register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if not User.login_is_valid(request.form):
            return redirect(url_for('auth.login'))

        user = User.find_user_by_email(request.form['email'])
        if not user:
            flash('Invalid credentials.', 'auth')
            return redirect(url_for('auth.login'))

        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash('Invalid credentials.', 'auth')
            return redirect(url_for('auth.login'))

        session['user_id'] = user.id
        return redirect(url_for('all_pets'))
    return render_template("/users/login.html")


@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))
