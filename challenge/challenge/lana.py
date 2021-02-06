from flask import Flask, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin

PRODUCTS = [
	{'code': 'PEN', 'name': 'Lana Pen', 'price': 500},
	{'code': 'TSHIRT', 'name': 'Lana T-Shirt', 'price': 2000},
	{'code': 'MUG', 'name': 'Lana Coffee Mug', 'price': 750},
]

def create_basket():
	db.session.add(Basket())
	db.session.commit()
	
def create_products():
	for p in PRODUCTS:
		db.session.add(Product(code=p['code'], name=p['name'], price=p['price']))
	db.session.commit()

# Initialize app using an in-memory SQLite database.
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
db = SQLAlchemy(app)

# Models
class Basket(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	basket_products = db.relationship("BasketProduct", backref="basket")
	
class BasketProduct(db.Model, SerializerMixin):
	basket_id = db.Column(db.Integer, db.ForeignKey('basket.id'), primary_key=True)
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), primary_key=True)
	quantity = db.Column(db.Numeric(2, 0)) # 2 digits, no decimals.
	
	product = db.relationship("Product")
	
	# Exclude those fields when serializing, for a lighter representation and
	# to avoid recursion issues as there are circular references between models.
	serialize_rules = ('-basket', '-basket_id', '-product.baskets', '-product_id')

class Product(db.Model, SerializerMixin):
	id = db.Column(db.Integer, primary_key=True)
	code = db.Column(db.String, unique=True, nullable=False)
	name = db.Column(db.String, nullable=False)
	price = db.Column(db.Numeric(10, 2)) # 10 digits, 2 of them are decimals.
	
	baskets = db.relationship('Basket', secondary=BasketProduct.__table__, lazy="select", viewonly=True)
	
	# Exclude baskets from serialization.
	serialize_rules = ('-baskets',)
	
	
# Create database tables
db.create_all()
db.session.commit()

create_products()
create_basket()

@app.route('/baskets/', methods=['POST'])
def create_basket():
	basket = Basket()
	db.session.add(basket)
	db.session.commit()
	return {'basket_id': basket.id}
	
# It's a bit ugly passing everything in the URL but I wanted to make it simpler. 
# In production I would pass the product and quantity as a JSON payload in the body.
@app.route('/baskets/<int:basket_id>/<int:product_id>/<int:quantity>', methods=['POST'])
def add_product_to_basket(basket_id, product_id, quantity):
	# Check that the provided basket and product exist.
	basket = Basket.query.get(basket_id)
	if not basket:
		return make_response(jsonify('Basket not found'), 404)
	product = Product.query.get(product_id)
	if not product:
		return make_response(jsonify('Product not found'), 404)
	
	# If BasketProduct already exists, update quantity, if not, create.
	basket_product = BasketProduct.query.filter_by(basket_id=basket_id, product_id=product_id).first()
	if basket_product:
		basket_product.quantity = quantity
	else:
		basket.basket_products.append(BasketProduct(basket_id=basket_id, product_id=product_id, quantity=quantity))
		
	db.session.commit()
	return basket.to_dict()
		
	
@app.route('/products/', methods=['GET'])
def get_products():
	return {'products': [p.to_dict() for p in Product.query.all()]}