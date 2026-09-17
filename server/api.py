from flask import Flask, jsonify, request, Response
from database import Database
import argparse


def create_app(db_file: str) -> Flask:
    app = Flask(__name__)
    db = Database(db_file)

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


    @app.route("/", methods=["GET"])
    def view_database():
        users = db.get_all_users()
        products = db.get_all_products()

        users_html = "".join(
            f"<tr><td>{u['id']}</td><td>{u['name']}</td>"
            f"<td>{u['email']}</td><td>{u['age']}</td></tr>"
            for u in users
        )

        products_html = "".join(
            f"<tr><td>{p['id']}</td><td>{p['name']}</td>"
            f"<td>{p['price']}</td><td>{p['stock']}</td></tr>"
            for p in products
        )

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>JSON database</title>
            <style>
                body {{ font-family: Arial, sans-serif; font-size: 26px; margin: 30px;
                        color: #DCDCDC; background-color: #282828; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ font-size: 18px; border: 1px solid #000000; padding: 10px; }}
                th {{ font-size: 22px; background-color: #1C1C1C; color: #BBBBBB; }}
                tr:nth-child(even) {{ background-color: #363636; }}
            </style>
        </head>
        <body>
            <h1>JSON database viewer</h1>
            <p>Database: {db_file}</p>

            <h2>Users ({len(users)})</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Email</th><th>Age</th></tr>
                {users_html or "<tr><td colspan=4>No users</td></tr>"}
            </table>

            <h2>Products ({len(products)})</h2>
            <table>
                <tr><th>ID</th><th>Name</th><th>Price</th><th>Stock</th></tr>
                {products_html or "<tr><td colspan=4>No products</td></tr>"}
            </table>
        </body>
        </html>
        """
        return Response(html, mimetype="text/html")

    return app


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSON Database REST API Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port (default: 5000)")
    parser.add_argument("--db", default="base.json", help="Database file (default: base.json)")
    args = parser.parse_args()
    app = create_app(args.db)

    print(f"Server running on {args.host}:{args.port}")
    print(f"Database file: {args.db}")
    print("Available endpoints:")
    print("- GET/POST /api/users")
    print("- GET/PUT/DELETE /api/users/<id>")
    print("- GET/POST /api/products")
    print("- GET/DELETE /api/products/<id>")
    print("- GET /api/check_server")

    app.run(host=args.host, port=args.port)