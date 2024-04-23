#!/usr/bin/env python3
from .models import db, Sweet, Vendor, VendorSweet
from flask_migrate import Migrate
from flask import Flask, jsonify, request, make_response
from flask_restful import Api, Resource
import os

# Create Flask app instance
app = Flask(__name__)

# Define the base directory and database URI
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")

# Configure the Flask app with database URI and settings
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Initialize Flask-RESTful API
api = Api(app)

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Define route for home page
@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

# Define route to get all vendors
@app.route('/vendors')
def get_vendors():
    vendors = Vendor.query.all()
    return jsonify([{
        'id': vendor.id,
        'name': vendor.name
    } for vendor in vendors]), 200

# Define route to get a specific vendor by ID
@app.route('/vendors/<int:id>', methods=['GET'])
def get_vendor(id):
    vendor = db.session.get(Vendor, id)
    if vendor is None:
        return jsonify({"error": "Vendor not found"}), 404
    return jsonify({
        "id": vendor.id,
        "name": vendor.name,
        "vendor_sweets": [vs.serialize() for vs in vendor.vendor_sweets]
    }), 200

# Define route to get all sweets
@app.route("/sweets", methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([sweet.serialize() for sweet in sweets]), 200

# Define route to get a specific sweet by ID
@app.route("/sweets/<int:id>", methods=['GET'])
def get_sweet(id):
    sweet = db.session.get(Sweet, id)
    if not sweet:
        return jsonify({"error": "Sweet not found"}), 404
    return jsonify(sweet.serialize()), 200

# Define route to delete a vendor sweet by ID
@app.route("/vendor_sweets/<int:id>", methods=['DELETE'])
def delete_vendor_sweet(id):
    vendor_sweet = db.session.get(VendorSweet, id)
    if not vendor_sweet:
        return jsonify({"error": "VendorSweet not found"}), 404
    try:
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({"message": "VendorSweet deleted"}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error: " + str(e)}), 500

# Define route to create a new vendor sweet
@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    data = request.get_json()
    price = data.get('price')
    vendor_id = data.get('vendor_id')
    sweet_id = data.get('sweet_id')

    # Validate input data
    if price is None or price < 0 or not vendor_id or not sweet_id:
        return make_response(jsonify({"errors": ["validation errors"]}), 400)

    # Create new VendorSweet instance
    new_vs = VendorSweet(price=price, vendor_id=vendor_id, sweet_id=sweet_id)
    db.session.add(new_vs)
    db.session.commit()  

    # Return response with newly created vendor sweet details
    return make_response(jsonify({
        "id": new_vs.id,
        "price": new_vs.price,
        "sweet": {"id": new_vs.sweet.id, "name": new_vs.sweet.name},
        "sweet_id": sweet_id,
        "vendor": {"id": new_vs.vendor.id, "name": new_vs.vendor.name},
        "vendor_id": vendor_id
    }), 201)
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)
