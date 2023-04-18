"""Blogly application."""

from flask import Flask, request, redirect, render_template

from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# debug = DebugToolbarExtension(app)
connect_db(app)

@app.route('/')
def display_home():
    """Display all posts"""
    posts = Post.query.all()
    return render_template('base.html', posts = posts)

@app.route('/users')
def list_users():
    """Shows list of all users in db"""
    users = User.query.all()
    return render_template('users.html', users=users)

@app.route('/users/new')
def display_form():
    """Display form to add user"""
    return render_template('add_user.html')

@app.route('/users/new', methods=["POST"])
def create_user():
    """Add new user"""
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
    user = User.query.filter_by(id=user_id).first()
    user.first_name = request.form["first-name"]
    user.last_name = request.form["last-name"]
    user.image_url = request.form["image-url"]
    db.session.commit()
    return redirect (f'/{user.id}')

@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show details about a post"""
    post = Post.query.get_or_404(post_id)
    tags = post.tags
    return render_template("post_details.html", post=post, tags=tags)

@app.route("/users/<int:user_id>/posts/new")  
def add_post_form(user_id):
    """Display add new post form"""
    tags = Tag.query.all()
    return render_template("add_edit_post.html", form_title = "Add new post", tags = tags)

@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def add_post(user_id):
    """Add new post"""
    title = request.form["title"]
    content = request.form["content"]
    tagInput = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tagInput)).all()
    new_post = Post(title=title,content=content,user_id=user_id, tags = tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect (f'/users/{user_id}')

@app.route("/posts/<int:post_id>/edit")
def edit_post_form(post_id):
    """Display edit post form"""
    tags = Tag.query.all()
    post = Post.query.filter_by(id=post_id).first()
    return render_template("add_edit_post.html", post = post, form_title = "Edit post", tags=tags )

@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def edit_post(post_id):
    """Edit post"""
    tagInput = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tagInput)).all()
    post = Post.query.get_or_404(post_id)
    post.title = request.form["title"]
    post.content = request.form["content"]
    post.tags = tags
    db.session.commit()
    return redirect (f'/posts/{post_id}')

@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Delete post"""
    post = Post.query.filter_by(id=post_id).first()
    db.session.delete(post)
    db.session.commit()
    print(f"<<<<<{post.user_id}>>>>>>")
    return redirect (f'/users/{post.user_id}')

@app.route("/tags")
def display_tags():
    """Display all tags"""
    tags = Tag.query.all()
    return render_template("tags.html", tags = tags)

@app.route("/tags/<int:tag_id>")
def display_tag_details(tag_id):
    """Display tag details"""
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template("tag_details.html", tag = tag, posts=posts)

@app.route("/tags/new")
def add_tag_form():
    """Display add tag form"""
    return render_template("add_edit_tag.html", form_title = "Add tag")

@app.route("/tags/new", methods=["POST"])
def add_tag():
    """Add tag"""
    name = request.form["name"]
    tag = Tag(name = name)
    db.session.add(tag)
    db.session.commit()
    return redirect (f'/tags')

@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Display edit tag form"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("add_edit_tag.html", tag = tag, form_title = "Edit tag")

@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form["name"]
    db.session.commit()
    return redirect (f'/tags/{tag_id}')

@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag"""
    tag = Tag.query.filter_by(id=tag_id).first()
    db.session.delete(tag)
    db.session.commit()
    return redirect ('/tags')