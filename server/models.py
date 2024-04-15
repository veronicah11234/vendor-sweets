from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData, Column, Integer, ForeignKey, CheckConstraint
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import relationship

db = SQLAlchemy()

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

class Sweet(db.Model, SerializerMixin):
    __tablename__ = 'sweets'

    id = Column(Integer, primary_key=True)
    name = Column(db.String)

    vendor_sweets = relationship('VendorSweet', back_populates='sweet')

    def __repr__(self):
        return f'<Sweet {self.id}>'

    def serialize(self, include_vendor_sweets=False):
        serialized_data = {
            'id': self.id,
            'name': self.name
        }
        if include_vendor_sweets:
            serialized_data['vendor_sweets'] = [vendor_sweet.serialize() for vendor_sweet in self.vendor_sweets]
        return serialized_data

class Vendor(db.Model, SerializerMixin):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True)
    name = Column(db.String)

    vendor_sweets = relationship('VendorSweet', back_populates='vendor')

    def __repr__(self):
        return f'<Vendor {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'vendor_sweets': [vendor_sweet.serialize() for vendor_sweet in self.vendor_sweets]
        }


class VendorSweet(db.Model, SerializerMixin):
    __tablename__ = 'vendor_sweets'

    id = Column(Integer, primary_key=True)
    price = Column(Integer, nullable=False)
    sweet_id = Column(Integer, ForeignKey('sweets.id'), nullable=False)
    vendor_id = Column(Integer, ForeignKey('vendors.id'), nullable=False)

    sweet = relationship('Sweet', back_populates='vendor_sweets')
    vendor = relationship('Vendor', back_populates='vendor_sweets')

    __table_args__ = (
        CheckConstraint('price >= 0', name='check_price_positive'),
    )

    def __repr__(self):
        return f'<VendorSweet {self.id}>'

    def serialize(self):
        return {
            'id': self.id,
            'price': self.price,
            'sweet': self.sweet.serialize(),
            'vendor': self.vendor.serialize()
        }
