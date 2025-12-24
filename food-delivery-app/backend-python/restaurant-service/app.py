from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///restaurants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20))

with app.app_context():
    db.create_all()

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return jsonify([{
        'id': r.id,
        'name': r.name,
        'address': r.address,
        'phone': r.phone
    } for r in restaurants])

@app.route('/api/restaurants', methods=['POST'])
def add_restaurant():
    data = request.json
    restaurant = Restaurant(
        name=data['name'],
        address=data['address'],
        phone=data.get('phone')
    )
    db.session.add(restaurant)
    db.session.commit()
    return jsonify({'id': restaurant.id, 'message': 'Restaurant added'}), 201

if __name__ == '__main__':
    app.run(port=8001, debug=True)
