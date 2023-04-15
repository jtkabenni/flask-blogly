"""Blogly application."""

from flask import Flask, request, redirect, render_template

from models import db, connect_db, User, Post

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
    """Create new user"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"] if request.form["image-url"] else None
    new_user  = User(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/users/{new_user.id}')

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a user"""
    user = User.query.get_or_404(user_id)
    posts = user.posts if user.posts else None
    posts = user.posts
    return render_template("user_details.html", user=user, posts=posts)

@app.route("/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect ('/users')

@app.route("/<int:user_id>/edit")
def edit_user_form(user_id):
    """Display edit user form"""
    user = User.query.get_or_404(user_id)
    return render_template("edit_user.html", user=user)

@app.route("/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Edit user"""
    first_name = request.form["first-name"]
    last_name = request.form["last-name"]
    image_url = request.form["image-url"]
    user = User.query.filter_by(id=user_id).first()
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()
    return redirect (f'/{user.id}')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a post"""
    post = Post.query.get_or_404(post_id)
    return render_template("post_details.html", post=post)

@app.route("/users/<int:user_id>/posts/new")  
def add_post_form(user_id):
    """Display add new post form"""
    return render_template("add_edit_post.html", form_title = "Add new post")

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add new post"""
    title = request.form["title"]
    content = request.form["content"]
    new_post = Post(title=title,content=content,user_id=user_id)
    print(title, content)
    db.session.add(new_post)
    db.session.commit()
    return redirect (f'/users/{user_id}')


@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Display edit post form"""
    post = Post.query.filter_by(id=post_id).first()
    return render_template("add_edit_post.html", post = post, form_title = "Edit post" )


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
  """Edit post"""
    title = request.form["title"]
    content = request.form["content"]
    post = Post.query.filter_by(id=post_id).first()
    post.title = title
    post.content = content
    db.session.commit()
    return redirect (f'/posts/{post_id}')



@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).delete()

    db.session.commit()
    return redirect ('/users')
