from flask_app import app
from flask_app.models.pet import Pet
from flask_app.middleware import login_required
from flask import (
    abort,
    g,
    redirect,
    render_template,
    request,
    url_for
)


@app.get("/")
def index():
    """ Renders the home page. """
    return render_template("/pets/index.html")


@app.get("/pets")
@login_required
def all_pets():
    """ Finds all the pets and displays them. """
    pets = Pet.find_all_pets()
    user = g.user
    return render_template("/pets/all_pets.html", pets=pets, user=user)


@app.route("/pets/new", methods=["GET", "POST"])
@login_required
def new_pet():
    """ GET: Displays new pet form. POST: Processes new pet form. """
    if request.method == "POST":
        print(f"{'*'*10}  {'*'*10}")
        print(request.form)
        print(f"{'*'*10}  {'*'*10}")
        if not Pet.pet_is_valid(request.form):
            return redirect(url_for("new_pet"))
        Pet.create_pet(request.form)
        return redirect(url_for("all_pets"))
    return render_template("/pets/new_pet.html")


@app.get("/pets/<int:pet_id>")
@login_required
def one_pet(pet_id):
    """ Displays details for one pet. """
    pet = Pet.find_one_pet(pet_id)
    if pet is None:
        return abort(404)
    return render_template("/pets/one_pet.html", pet=pet)


@app.route("/pets/<int:pet_id>/edit", methods=["GET", "POST"])
@login_required
def edit_pet(pet_id):
    """ GET: Displays edit pet form. POST: Processes edit pet form. """
    if request.method == "POST":
        if not Pet.pet_is_valid(request.form):
            return redirect(url_for("edit_pet", pet_id=pet_id))
        Pet.update_one_pet(request.form)
        return redirect(url_for("one_pet", pet_id=pet_id))
    pet = Pet.find_one_pet(pet_id)
    if pet is None:
        abort(404)
    return render_template("/pets/edit_pet.html", pet=pet)


@app.post("/pets/<int:pet_id>/delete")
@login_required
def delete_pet(pet_id):
    """ Deletes one pet by ID. """
    pet = Pet.find_one_pet(pet_id)
    if pet is None:
        abort(404)
    Pet.delete_one_pet(pet_id)
    return redirect(url_for("all_pets"))


@app.errorhandler(404)
def not_found(e):
    """ 404 not found custom page. """
    return render_template("/pets/404.html", e=e)
