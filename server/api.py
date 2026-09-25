from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import uvicorn
import database
import argparse

app = FastAPI()

DB_HOST = "localhost"
DB_NAME = "base"
DB_USER = "user"
DB_PASSWORD = "password"

class CreateUser(BaseModel):
    name: str
    email: str
    age: Optional[int] = 0


class UpdateUser(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None


class CreateProduct(BaseModel):
    name: str
    price: float
    stock: int
    number_of_purchases: Optional[int] = 0


class UpdateProduct(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    stock: Optional[int] = None
    number_of_purchases: Optional[int] = None


#===================
#====== USERS ======
#===================

@app.post("/api/users")
async  def create_user(user: CreateUser):
    result = await database.create_user(name=user.name, email=user.email, age=user.age)
    return result


@app.get("/api/users")
async def get_all_users():
    return await database.get_all_users()


@app.get("/api/users/{user_id}")
async def get_user_by_id(user_id: int):
    user = await database.get_user_by_id(user_id)
    if user:
        return user
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/api/users/{user_id}")
async def update_user_by_id(user_id: int, user: UpdateUser):
    update_data = {k: v for k, v in user.model_dump().items() if v is not None}
    result = await database.update_user_by_id(user_id, **update_data)
    if result:
        return result
    raise HTTPException(status_code=404, detail="User not found")


@app.delete("/api/users/{user_id}")
async def delete_user_by_id(user_id: int):
    result = await database.delete_user_by_id(user_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="User not found")


#====================
#===== PRODUCTS =====
#====================

@app.post("/api/products")
async def create_product(product: CreateProduct):
    result = await database.create_product(
        name=product.name,
        price=product.price,
        stock=product.stock,
        number_of_purchases=product.number_of_purchases
    )
    return result


@app.get("/api/products")
async def get_all_products():
    return await database.get_all_products()


@app.get("/api/products/{product_id}")
async def get_product_by_id(product_id: int):
    product = await database.get_product_by_id(product_id)
    if product:
        return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/api/products/{product_id}")
async def update_product_by_id(product_id: int, product: UpdateProduct):
    update_data = {k: v for k, v in product.model_dump().items() if v is not None}
    result = await database.update_product_by_id(product_id, **update_data)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/api/products/{product_id}")
async def delete_product_by_id(product_id: int):
    result = await database.delete_product_by_id(product_id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Product not found")


@app.get("/api/check_server")
async def check_server_check():
    return {"status": "ok", "message": "PostgreSQL Database API is running"}


@app.get("/")
async def view_database():
    users = await database.get_all_users()
    products = await database.get_all_products()

    users_html = "".join(
        f"<tr><td>{u['id']}</td><td>{u['name']}</td>"
        f"<td>{u['email']}</td><td>{u['age']}</td></tr>"
        for u in users
    )

    products_html = "".join(
        f"<tr><td>{p['id']}</td><td>{p['name']}</td><td>{p['price']}</td>"
        f"<td>{p['stock']}</td><td>{p['number_of_purchases']}</td></tr>"
        for p in products
    )

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>PostgreSQL database</title>
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
        <h1>PostgreSQL database viewer</h1>

        <h2>Users ({len(users)})</h2>
        <table>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Age</th></tr>
            {users_html or "<tr><td colspan=4>No users</td></tr>"}
        </table>

        <h2>Products ({len(products)})</h2>
        <table>
            <tr><th>ID</th><th>Name</th><th>Price</th>
            <th>Stock</th><th>Number of purchases</th></tr>
            {products_html or "<tr><td colspan=5>No products</td></tr>"}
        </table>
    </body>
    </html>
    """
    return Response(html, media_type="text/html")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PostgreSQL Database REST API Server")
    parser.add_argument("--host", default="127.0.0.1", help="Host (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=5000, help="Port (default: 5000)")
    parser.add_argument("--db", default="base", help="Database name (default: base)")
    parser.add_argument("--db-user", default="user", help="Database user (default: user)")
    parser.add_argument("--db-pass", default="password", help="Database password (default: password)")
    args = parser.parse_args()

    database.DB_HOST = args.host
    database.DB_NAME = args.db
    database.DB_USER = args.db_user
    database.DB_PASSWORD = args.db_pass

    print(f"Server running on {args.host}:{args.port}")
    print(f"Database: {args.db}")
    print("Available endpoints:")
    print("- GET/POST /api/users")
    print("- GET/PUT/DELETE /api/users/<id>")
    print("- GET/POST /api/products")
    print("- GET/DELETE /api/products/<id>")
    print("- GET /api/check_server")

    uvicorn.run(app, host=args.host, port=args.port)