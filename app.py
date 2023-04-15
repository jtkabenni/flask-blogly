"""Blogly application."""

from flask import Flask, request, redirect, render_template

from models import db, connect_db, User

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def display_home():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('base.html', users=users)

@app.route('/users/new')
def display_form():
    """Shows list of all users in db"""
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/{new_user.id}')

@app.route("/<int:user_id>")
def show_pet(user_id):
    """Show details about a single pet"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route("/<int:user_id>/delete", methods=["POST"])
def delete_user_form(user_id):
    user = User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect ('/users')

@app.route("/<int:user_id>/edit")
def edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    user = User.query.filter_by(id=user_id).first()
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()
    return redirect (f'/{user.id}')


