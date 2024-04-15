from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
from sqlalchemy.orm.exc import NoResultFound
from server.models import Sweet, Vendor, VendorSweet, db
# from . import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)
migrate = Migrate(app, db)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    return '<h1>Code challenge</h1>'

@app.route('/sweets', methods=['GET'])
def get_sweets():
    sweets = Sweet.query.all()
    return jsonify([sweet.serialize() for sweet in sweets])

@app.route('/sweets/<int:sweet_id>', methods=['GET'])
def get_sweet(sweet_id):
    try:
        sweet = Sweet.query.filter_by(id=sweet_id).one()
        return jsonify(sweet.serialize())
    except NoResultFound:
        return jsonify({"error": "Sweet not found"}), 404


@app.route('/vendors', methods=['GET'])
def get_vendors():
    try:
        logger.info("Attempting to retrieve vendors...")
        vendors = Vendor.query.all()
        logger.info("Vendors retrieved successfully.")
        return jsonify([vendor.serialize() for vendor in vendors]), 200
    except Exception as e:
        # Log the exception for debugging purposes
        logger.error(f"An error occurred while retrieving vendors: {str(e)}")
        # Return an appropriate error response
        return jsonify({"error": "Internal Server Error"}), 500

@app.route('/vendors/<int:vendor_id>', methods=['GET'])
def get_vendor(vendor_id):
    try:
        vendor = Vendor.query.filter_by(id=vendor_id).one()
        return jsonify(vendor.serialize())
    except NoResultFound:
        return jsonify({"error": "Vendor not found"}), 404

@app.route('/vendor_sweets', methods=['POST'])
def create_vendor_sweet():
    try:
        data = request.json
        sweet_id = data.get('sweet_id')
        vendor_id = data.get('vendor_id')
        price = data.get('price')

        # Check if all required fields are provided
        if not all([sweet_id, vendor_id, price]):
            return jsonify({"error": "sweet_id, vendor_id, and price are required"}), 400

        # Check if sweet and vendor exist
        sweet = Sweet.query.get(sweet_id)
        vendor = Vendor.query.get(vendor_id)
        if not sweet:
            return jsonify({"error": "Sweet not found"}), 404
        if not vendor:
            return jsonify({"error": "Vendor not found"}), 404

        # Create and add the VendorSweet instance to the database
        vendor_sweet = VendorSweet(sweet_id=sweet_id, vendor_id=vendor_id, price=price)
        db.session.add(vendor_sweet)
        db.session.commit()

        # Return the serialized VendorSweet instance with status code 201
        return jsonify(vendor_sweet.serialize()), 201

    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred while creating VendorSweet: {str(e)}")
        # Return an appropriate error response
        return jsonify({"error": "Failed to create VendorSweet"}), 400

@app.route('/vendor_sweets/<int:vendor_sweet_id>', methods=['DELETE'])
def delete_vendor_sweet(vendor_sweet_id):
    try:
        vendor_sweet = VendorSweet.query.filter_by(id=vendor_sweet_id).one()
        db.session.delete(vendor_sweet)
        db.session.commit()
        return jsonify({}), 204
    except NoResultFound:
        return jsonify({"error": "VendorSweet not found"}), 404

