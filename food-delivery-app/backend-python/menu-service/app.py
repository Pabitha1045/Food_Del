from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///menus.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    restaurant_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/menus/<int:restaurant_id>', methods=['GET'])
def get_menu(restaurant_id):
    menu_items = MenuItem.query.filter_by(restaurant_id=restaurant_id).all()
    return jsonify([{
        'id': m.id,
        'name': m.name,
        'description': m.description,
        'price': m.price
    } for m in menu_items])

@app.route('/api/menus', methods=['POST'])
def add_menu_item():
    data = request.json
    menu_item = MenuItem(
        restaurant_id=data['restaurant_id'],
        name=data['name'],
        description=data.get('description'),
        price=data['price']
    )
    db.session.add(menu_item)
    db.session.commit()
    return jsonify({'id': menu_item.id, 'message': 'Menu item added'}), 201

if __name__ == '__main__':
    app.run(port=8002, debug=True)
