from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db = SQLAlchemy(app)

class Basket(db.Model):
	id = db.Column(db.Integer, primary_key=True)

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	price = db.Column(db.Integer)
	
db.create_all()
db.session.commit()

@app.route('/baskets/', methods=['POST'])
def create_basket():
	basket = Basket()
	db.session.add(basket)
	db.session.commit()
	return {'basket_id': basket.id}