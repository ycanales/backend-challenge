from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

PRODUCTS = [
	{'code': 'PEN', 'name': 'Lana Pen', 'price': 500},
	{'code': 'TSHIRT', 'name': 'Lana T-Shirt', 'price': 2000},
	{'code': 'MUG', 'name': 'Lana Coffee Mug', 'price': 750},
]

def create_products():
	for p in PRODUCTS:
		db.session.add(Product(code=p['code'], name=p['name'], price=p['price']))
	db.session.commit()

# Initialize app using an in-memory SQLite database.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db = SQLAlchemy(app)

# Models
products = db.Table('products',
db.Column('basket_id', db.Integer, db.ForeignKey('basket.id'), primary_key=True),
db.Column('product_id', db.Integer, db.ForeignKey('product.id'))
)

class Basket(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	products = db.relationship('Product', secondary=products, lazy='subquery', backref=db.backref('baskets', lazy=True))

class Product(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	price = db.Column(db.Integer)
	
	
# Create database tables
db.create_all()
db.session.commit()

create_products()

@app.route('/baskets/', methods=['POST'])
def create_basket():
	basket = Basket()
	db.session.add(basket)
	db.session.commit()
	return {'basket_id': basket.id}
	
@app.route('/products/', methods=['GET'])
def get_products():
	return {'products': [p.to_dict() for p in Product.query.all()]}