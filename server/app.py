from flask import Flask, request, jsonify
from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery API</h1>'

@app.route('/bakeries/<int:id>', methods=['PATCH'])
def update_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    new_name = request.form.get('name')
    if new_name:
        bakery.name = new_name
        db.session.commit()
        return jsonify({'message': 'Bakery updated successfully'}), 200
    else:
        return jsonify({'error': 'Name not provided'}), 400

@app.route('/baked_goods', methods=['POST'])
def create_baked_good():
    name = request.form.get('name')
    price = request.form.get('price')
    if name and price:
        new_baked_good = BakedGood(name=name, price=price)
        db.session.add(new_baked_good)
        db.session.commit()
        return jsonify({'message': 'Baked good created successfully'}), 201
    else:
        return jsonify({'error': 'Name or price not provided'}), 400

@app.route('/baked_goods/<int:id>', methods=['DELETE'])
def delete_baked_good(id):
    baked_good = BakedGood.query.get_or_404(id)
    db.session.delete(baked_good)
    db.session.commit()
    return jsonify({'message': 'Baked good deleted successfully'}), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
