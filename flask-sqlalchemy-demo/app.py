from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__);
# ///表示使用相对目录。
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db';
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True;
db = SQLAlchemy(app);

class User(db.Model):
	"""定义数据模型"""
	__tablename__ = 'users';
	id = db.Column(db.Integer, primary_key=True);
	username = db.Column(db.String(80), unique=True);
	email = db.Column(db.String(120), unique=True);
	
	def __init__(self, username, email):
		self.username = username;
		self.email = email;
		
	def __repr__(self):
		return '<User %r>' % self.username
		
@app.route('/adduser')
def add_user():
	user1 = User('ethan', 'ethan@example.com');
	user2 = User('admin', 'admin@example.com');
	user3 = User('guest', 'guest@example.com');
	user4 = User('joe', 'joe@example.com');
	user5 = User('michael', 'michael@example.com');
	
	db.session.add(user1);
	db.session.add(user2);
	db.session.add(user3);
	db.session.add(user4);
	db.session.add(user5);
	
	db.session.commit();
	
	return "<p>add successfuly!";
	
if __name__ == "__main__":
	app.run();

