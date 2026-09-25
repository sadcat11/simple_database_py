import asyncpg
from typing import List, Dict, Optional


DB_HOST = "localhost"
DB_NAME = "base"
DB_USER = "user"
DB_PASSWORD = "password"


async def get_connection():
    return await asyncpg.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


#===================
#====== USERS ======
#===================


async def create_user(name: str, email: str, age: int) -> Dict:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "INSERT INTO users (name, email, age) "
            "VALUES ($1, $2, $3) RETURNING id, name, email, age",
            name, email, age
        )
        return {"id": row["id"], "name": row["name"], "email": row["email"], "age": row["age"]}

    finally:
        await conn.close()


async def get_all_users() -> List[Dict]:
    conn = await get_connection()
    try:
        rows = await conn.fetch("SELECT id, name, email, age FROM users")
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "name": r["name"],
                "email": r["email"],
                "age": r["age"]
            })
        return result

    finally:
        await conn.close()


async def get_user_by_id(user_id: int) -> Optional[Dict]:
    conn = await get_connection()
    try:
        row = await conn.fetchrow("SELECT id, name, email, age FROM users WHERE id = $1", user_id)
        if row:
            return {"id": row["id"], "name": row["name"], "email": row["email"], "age": row["age"]}
        else:
            return None

    finally:
        await conn.close()


async def update_user_by_id(user_id: int, **kwargs) -> Optional[Dict]:
    conn = await get_connection()
    try:
        # Build dynamic update query
        updates = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = ${len(values) + 1}")
                values.append(value)

        if not updates:
            return None

        values.append(user_id)
        query = (f"UPDATE users SET {', '.join(updates)} "
                 f"WHERE id = ${len(values)} RETURNING id, name, email, age")
        row = await conn.fetchrow(query, *values)
        if row:
            return {"id": row["id"], "name": row["name"], "email": row["email"], "age": row["age"]}
        else:
            return None

    finally:
        await conn.close()


async def delete_user_by_id(user_id: int) -> Optional[Dict]:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "DELETE FROM users "
            "WHERE id = $1 RETURNING id, name, email, age",
            user_id
        )
        if row:
            return {"id": row["id"], "name": row["name"], "email": row["email"], "age": row["age"]}
        else:
            return None

    finally:
        await conn.close()


#====================
#===== PRODUCTS =====
#====================


async def create_product(name: str, price: float, stock: int, number_of_purchases: int) -> Dict:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "INSERT INTO products (name, price, stock, number_of_purchases) "
            "VALUES ($1, $2, $3, $4) RETURNING id, name, price, stock, number_of_purchases",
            name, price, stock, number_of_purchases
        )
        return {"id": row["id"],
                "name": row["name"],
                "price": row["price"],
                "stock": row["stock"],
                "number_of_purchases": row["number_of_purchases"]}

    finally:
        await conn.close()


async def get_all_products() -> List[Dict]:
    conn = await get_connection()
    try:
        rows = await conn.fetch("SELECT id, name, price, stock, number_of_purchases "
                                "FROM products")
        result = []
        for r in rows:
            result.append({
                "id": r["id"],
                "name": r["name"],
                "price": r["price"],
                "stock": r["stock"],
                "number_of_purchases": r["number_of_purchases"]
            })
        return result

    finally:
        await conn.close()


async def get_product_by_id(product_id: int) -> Optional[Dict]:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "SELECT id, name, price, stock, number_of_purchases "
            "FROM products WHERE id = $1",
            product_id
        )
        if row:
            return {"id": row["id"],
                    "name": row["name"],
                    "price": row["price"],
                    "stock": row["stock"],
                    "number_of_purchases": row["number_of_purchases"]}
        else:
            return None

    finally:
        await conn.close()


async def update_product_by_id(product_id: int, **kwargs) -> Optional[Dict]:
    conn = await get_connection()
    try:
        # Build dynamic update query
        updates = []
        values = []
        for key, value in kwargs.items():
            if value is not None:
                updates.append(f"{key} = ${len(values) + 1}")
                values.append(value)

        if not updates:
            return None

        values.append(product_id)
        query = (f"UPDATE products SET {', '.join(updates)} "
                 f"WHERE id = ${len(values)} RETURNING id, name, price, stock, number_of_purchases")
        row = await conn.fetchrow(query, *values)
        if row:
            return {"id": row["id"],
                    "name": row["name"],
                    "price": row["price"],
                    "stock": row["stock"],
                    "number_of_purchases": row["number_of_purchases"]}
        else:
            return None

    finally:
        await conn.close()


async def delete_product_by_id(product_id: int) -> Optional[Dict]:
    conn = await get_connection()
    try:
        row = await conn.fetchrow(
            "DELETE FROM products "
            "WHERE id = $1 RETURNING id, name, price, stock, number_of_purchases",
            product_id
        )
        if row:
            return {"id": row["id"],
                    "name": row["name"],
                    "price": row["price"],
                    "stock": row["stock"],
                    "number_of_purchases": row["number_of_purchases"]}
        else:
            return None

    finally:
        await conn.close()