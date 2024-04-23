# Flask Code Challenge - Sweets Vendors
- Install dependencies:
    pip install -r requirements.txt

- Usage
Run the Flask app:
   python3 app.py

- Access the API endpoints:
    Home: http://localhost:5555/
    Get all vendors: http://localhost:5555/vendors
    Get vendor by ID: http://localhost:5555/vendors/<vendor_id>
    Get all sweets: http://localhost:5555/sweets
    Get sweet by ID: http://localhost:5555/sweets/<sweet_id>
    Delete vendor sweet by ID: http://localhost:5555/vendor_sweets/<vendor_sweet_id>
    Create new vendor sweet: Send a POST request to http://localhost:5555/vendor_sweets with JSON data:

{
    "price": 10,
    "vendor_id": 1,
    "sweet_id": 1
}

# Models
- Sweet
  Attributes:
    id: Primary key (Integer)
    name: Name of the sweet (String)
# Vendor
  Attributes:
    id: Primary key (Integer)
    name: Name of the vendor (String)
# VendorSweet
  Attributes:
    id: Primary key (Integer)
    price: Price of the sweet from the vendor (Integer)
    sweet_id: Foreign key referencing Sweet table (Integer)
    vendor_id: Foreign key referencing Vendor table (Integer)

# Contributing
Contributions are welcome! Please open an issue or submit a pull request with any improvements or bug fixes.

# Author
Miriam wangui
github- veronicah11234

# License
This project is licensed under the MIT License.