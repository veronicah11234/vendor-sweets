import pytest
from server.app import app
from models import db, Sweet, Vendor, VendorSweet
from faker import Faker
from flask import Flask

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
    return app

class TestVendorSweet:
    '''Class VendorSweet in models.py'''

    def test_price_0_or_greater(self, app):
        '''requires price >= 0.'''

        with app.app_context():
            sweet = Sweet(name=Faker().name())
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            # Create a VendorSweet instance with price 0
            vendor_sweet = VendorSweet(vendor_id=vendor.id, sweet_id=sweet.id, price=0)
            db.session.add(vendor_sweet)
            db.session.commit()

    def test_price_too_low(self, app):
        '''requires non negative price .'''

        with app.app_context():
            sweet = Sweet(name=Faker().name())
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            # Create a VendorSweet instance with a negative price
            with pytest.raises(ValueError):
                vendor_sweet = VendorSweet(vendor_id=vendor.id, sweet_id=sweet.id, price=-1)
                db.session.add(vendor_sweet)
                db.session.commit()

    def test_price_none(self, app):
        '''requires non negative price .'''

        with app.app_context():
            sweet = Sweet(name=Faker().name())
            vendor = Vendor(name=Faker().name())
            db.session.add_all([sweet, vendor])
            db.session.commit()

            # Create a VendorSweet with None price
            with pytest.raises(ValueError):
                vendor_sweet = VendorSweet(vendor_id=vendor.id, sweet_id=sweet.id, price=None)
                db.session.add(vendor_sweet)
                db.session.commit()
