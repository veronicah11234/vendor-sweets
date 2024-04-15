from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

# Create the metadata object with naming conventions for constraints
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# Initialize SQLAlchemy with metadata
db = SQLAlchemy(metadata=metadata)

class Sweet(db.Model, SerializerMixin):
    """Model class representing sweets."""
    __tablename__ = 'sweets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)  # Define maximum length for String
    vendor_sweets = db.relationship("VendorSweet", back_populates="sweet")

    def serialize(self):
        """Serialize the Sweet object."""
        return {"id": self.id, "name": self.name}

class Vendor(db.Model, SerializerMixin):
    """Model class representing vendors."""
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))  # Define maximum length for String
    vendor_sweets = db.relationship("VendorSweet", back_populates="vendor")

    def serialize(self):
        """Serialize the Vendor object."""
        return {"id": self.id, "name": self.name}

class VendorSweet(db.Model, SerializerMixin):
    """Model class representing the association between vendors and sweets."""
    __tablename__ = 'vendor_sweets'
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    sweet_id = db.Column(db.Integer, db.ForeignKey("sweets.id"), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendors.id"), nullable=False)
    sweet = db.relationship("Sweet", back_populates="vendor_sweets")
    vendor = db.relationship("Vendor", back_populates="vendor_sweets")

    def serialize(self):
        """Serialize the VendorSweet object."""
        return {
            "id": self.id,
            "price": self.price,
            "sweet": self.sweet.serialize(),
            "vendor": self.vendor.serialize()
        }

    @validates('price')
    def validate_price(self, key, price):
        """Validate the price attribute."""
        if price is None:
            raise ValueError("Price cannot be None")
        if price < 0:
            raise ValueError("Price must be non-negative")
        return price

    def __repr__(self):
        """String representation of VendorSweet object."""
        return f'<VendorSweet id={self.id}, price={self.price}, vendor_id={self.vendor_id}, sweet_id={self.sweet_id}>'
