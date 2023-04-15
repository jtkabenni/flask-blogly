from models import User, Post, db
from app import app

db.drop_all()
db.create_all()

bean =  User(first_name = 'Bean', last_name = "Bo", image_url = "http://clipart-library.com/img/1015367.jpg")
lizzie=  User(first_name = 'Lizzie', last_name = "Pusheen", image_url = "http://clipart-library.com/img/1015367.jpg")
orange =  User(first_name = 'Orange', last_name = "Pop", image_url = "https://www.kindpng.com/picc/m/50-507122_thinking-woman-cartoon-girl-clip-art-clipart-transparent.png")

db.session.add_all([bean, lizzie, orange])
db.session.commit()

post1 = Post(title = 'My title', content = 'My content', user_id = 1)
post2 = Post(title = 'My second title', content = 'My second content My second contentMy second contentMy second contentMy second contentMy second content', user_id = 1)
post3 = Post(title = 'Lizzie''s first title', content = 'My first post!!!', user_id = 2)
db.session.add_all([post1, post2, post3])
db.session.commit()

