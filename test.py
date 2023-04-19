import unittest
from app import app
from models import db, User, Post, Tag, PostTag

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True


db.drop_all()
db.create_all()

class UserViewsTests(unittest.TestCase):
  def setUp(self):
    """Add sample user"""
    User.query.delete()
    user1 =  User(first_name = 'Bean', last_name = "Bo", image_url = "http://clipart-library.com/img/1015367.jpg")
    db.session.add(user1)
    db.session.commit()
    self.user_id=user1.id
  def tearDown(self):
    """Roll back any changes"""
    db.session.rollback()

  def test_lists_users(self):
    """Test if user shows up in list"""
    with app.test_client() as client:
      resp = client.get("/users")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn('Bean Bo', html)
  def test_details_user(self):
    """ Test if user details show up on details page"""
    with app.test_client() as client:
      resp = client.get(f"/users/{self.user_id}")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn("Bean Bo's posts", html)

  def test_delete_user(self):
    """Test if user is deleted from users list"""
    with app.test_client() as client:
      resp = client.post(f"/users/{self.user_id}/delete", follow_redirects=True)
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertNotIn('Bean Bo', html)

class PostViewsTests(unittest.TestCase):
  def setUp(self):
    """Add sample user"""
    User.query.delete()
    user1 =  User(first_name = 'Bean', last_name = "Bo", image_url = "http://clipart-library.com/img/1015367.jpg")
    db.session.add(user1)
    db.session.commit()
    post1 = Post(title = 'My post title', content = 'My post content', user_id = user1.id)
    post2 = Post(title = 'My second post title', content = 'My second content', user_id = user1.id)
    db.session.add_all([post1,post2])
    db.session.commit()
    self.user_id=user1.id
    self.post1_id=post1.id
    self.post2_id=post2.id
  def tearDown(self):
    db.session.rollback()

  def test_lists_posts(self):
    """Test if posts shows up in list"""
    with app.test_client() as client:
      resp = client.get("/")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn('My post title', html)
      self.assertIn('My second post title', html)

  def test_details_post(self):
    """ Test if user details show up on details page"""
    with app.test_client() as client:
      resp = client.get(f"/posts/{self.post1_id}")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn('My post title', html)
      self.assertIn('<button>Edit post</button>', html)

  def test_delete_post(self):
    """Test if user is deleted from users list"""
    with app.test_client() as client:
      resp = client.post(f"/posts/{self.post1_id}/delete", follow_redirects=True)
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertNotIn('My post title', html)

class TagViewsTests(unittest.TestCase):
  def setUp(self):
    """Add sample user"""
    Post.query.delete()
    user1 =  User(first_name = 'Bean', last_name = "Bo", image_url = "http://clipart-library.com/img/1015367.jpg")
    db.session.add(user1)
    db.session.commit()
    post1 = Post(title = 'My post title', content = 'My content', user_id = user1.id)
    post2 = Post(title = 'My second title', content = 'My second content', user_id = user1.id)
    db.session.add_all([post1,post2])
    db.session.commit()
    tag1 = Tag(name = 'funny', posttags = [PostTag(post_id =post1.id), PostTag(post_id = post2.id)])
    tag2 = Tag(name = 'eww', posttags = [PostTag(post_id =post1.id)])
    db.session.add_all([tag1, tag2])
    db.session.commit()
    self.user_id=user1.id
    self.post1_id=post1.id
    self.post2_id=post2.id
    self.tag1_id=tag1.id
    self.tag2_id=tag2.id
  def tearDown(self):
    db.session.rollback()
  def test_lists_tags(self):
    with app.test_client() as client:
      resp = client.get("/tags")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn('funny', html)
      self.assertIn('eww', html)
  def test_details_tag(self):
    """ Test if tag details show up on tag details page"""
    with app.test_client() as client:
      resp = client.get(f"/tags/{self.tag1_id}")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn('funny', html)
      self.assertIn('Posts with this tag:', html)
    
  def test_post_details_tag(self):
    """ Test if user details show up on details page"""
    with app.test_client() as client:
      resp = client.get(f"/posts/{self.post1_id}")
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertIn('My post title', html)
      self.assertIn('<span class="tag">eww</span>', html)

  def test_delete_tag(self):
    """Test if tag is deleted from tags list"""
    with app.test_client() as client:
      resp = client.post(f"/tags/{self.tag1_id}/delete", follow_redirects=True)
      html = resp.get_data(as_text=True)
      self.assertEqual(resp.status_code, 200)
      self.assertNotIn('funny', html)

