from flask import Flask, jsonify, request
from database import Database

app = Flask(__name__)
db = Database()

#===================
#====== USERS ======
#===================
@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    name = data.get("name")
    email = data.get("email", "")
    age = data.get("age", 0)

    user = db.create_user(name=name, email=email, age=age)
    return jsonify(user), 201

@app.route("/api/users", methods=["GET"])
def get_all_users():
    return jsonify(db.get_all_users())

@app.route("/api/users/<int:user_id>", methods=["GET"])
def get_user_by_id(user_id):
    user = db.get_user_by_id(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/api/users/<int:user_id>", methods=["PUT"])
def update_user_by_id(user_id):
    update_data = request.get_json() or {}

    user = db.update_user_by_id(user_id, **update_data)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route("/api/users/<int:user_id>", methods=["DELETE"])
def delete_user_by_id(user_id):
    deleted = db.delete_user_by_id(user_id)
    if deleted:
        return jsonify(deleted)
    return jsonify({"error": "User not found"}), 404

#====================
#===== PRODUCTS =====
#====================
@app.route("/api/products", methods=["POST"])
def create_product():
    data = request.get_json()

    if not data or "name" not in data:
        return jsonify({"error": "Name is required"}), 400

    name = data.get("name")
    price = data.get("price", 0.0)
    stock = data.get("stock", 0)

    product = db.create_product(name=name, price=price, stock=stock)
    return jsonify(product), 201

@app.route("/api/products", methods=["GET"])
def get_all_products():
    return jsonify(db.get_all_products())

@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product_by_id(product_id):
    product = db.get_product_by_id(product_id)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route("/api/products/<int:product_id>", methods=["PUT"])
def update_product_by_id(product_id):
    update_data = request.get_json() or {}

    product = db.update_product_by_id(product_id, **update_data)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route("/api/products/<int:product_id>", methods=["DELETE"])
def delete_product_by_id(product_id):
    deleted = db.delete_product_by_id(product_id)
    if deleted:
        return jsonify(deleted)
    return jsonify({"error": "Product not found"}), 404

@app.route("/api/check_server", methods=["GET"])
def check_server_check():
    return jsonify({"status": "ok", "message": "JSON Database API is running"})

if __name__ == "__main__":
    print("Server running on http://localhost:5000")
    print("Available endpoints:")
    print("- GET/POST /api/users")
    print("- GET/PUT/DELETE /api/users/<id>")
    print("- GET/POST /api/products")
    print("- GET/DELETE /api/products/<id>")
    print("- GET /api/check_server")
    app.run(debug=True, port=5000)