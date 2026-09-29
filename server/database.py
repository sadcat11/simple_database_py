from typing import List, Dict, Optional
from sqlalchemy import insert, delete, select, update, Table, MetaData, Column, Integer, String, Numeric
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from sqlalchemy.exc import SQLAlchemyError

USER_FIELDS = {"name", "email", "age"}
PRODUCT_FIELDS = {"name", "price", "stock", "number_of_purchases"}


engine = None
metadata = MetaData()

users = Table(
    "users",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("email", String(255), nullable=False),
    Column("age", Integer, nullable=False, default=0),
)

products = Table(
    "products",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(100), nullable=False),
    Column("price", Numeric, nullable=False),  # Numeric для точности
    Column("stock", Integer, nullable=False),
    Column("number_of_purchases", Integer, nullable=False, default=0),
)


def init_database(host: str = "localhost", db_name: str = "base",
                  db_user: str = "user", db_password: str = "password"):
    global engine

    db_url = f"postgresql+asyncpg://{db_user}:{db_password}@{host}/{db_name}"
    engine = create_async_engine(db_url, echo=True)


async def get_connection() -> AsyncConnection:
    assert engine is not None, "Call init_database() first"
    return await engine.connect()


#===================
#====== USERS ======
#===================


async def create_user(name: str, email: str, age: int) -> Dict:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = insert(users).values(name=name, email=email, age=age).returning(
                users.c.id, users.c.name, users.c.email, users.c.age
            )
            result = await conn.execute(stmt)
            await conn.commit()
            row = result.fetchone()
            return {"id": row.id, "name": row.name, "email": row.email, "age": row.age}

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def get_all_users() -> List[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = select(users.c.id, users.c.name, users.c.email, users.c.age)
            result = await conn.execute(stmt)
            rows = result.fetchall()
            return [{"id": r.id, "name": r.name, "email": r.email, "age": r.age} for r in rows]

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def get_user_by_id(user_id: int) -> Optional[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = select(users.c.id, users.c.name, users.c.email, users.c.age).where(
                users.c.id == user_id
            )
            result = await conn.execute(stmt)
            row = result.fetchone()
            if row:
                return {"id": row.id, "name": row.name, "email": row.email, "age": row.age}
            return None

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def update_user_by_id(user_id: int, **kwargs) -> Optional[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            update_data = {
                key: value for key, value in kwargs.items()
                if value is not None and key in USER_FIELDS
            }

            if not update_data:
                return None

            stmt = (
                update(users)
                .where(users.c.id == user_id)
                .values(**update_data)
                .returning(users.c.id, users.c.name, users.c.email, users.c.age)
            )
            result = await conn.execute(stmt)
            await conn.commit()
            row = result.fetchone()
            if row:
                return {"id": row.id, "name": row.name, "email": row.email, "age": row.age}
            return None

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def delete_user_by_id(user_id: int) -> Optional[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = (
                delete(users)
                .where(users.c.id == user_id)
                .returning(users.c.id, users.c.name, users.c.email, users.c.age)
            )
            result = await conn.execute(stmt)
            await conn.commit()
            row = result.fetchone()
            if row:
                return {"id": row.id, "name": row.name, "email": row.email, "age": row.age}
            return None

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


#====================
#===== PRODUCTS =====
#====================


async def create_product(name: str, price: float, stock: int, number_of_purchases: int) -> Dict:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = insert(products).values(
                name=name,
                price=price,
                stock=stock,
                number_of_purchases=number_of_purchases
            ).returning(
                products.c.id,
                products.c.name,
                products.c.price,
                products.c.stock,
                products.c.number_of_purchases
            )
            result = await conn.execute(stmt)
            await conn.commit()
            row = result.fetchone()
            return {"id": row.id,
                    "name": row.name,
                    "price": row.price,
                    "stock": row.stock,
                    "number_of_purchases": row.number_of_purchases}

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def get_all_products() -> List[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = select(
                products.c.id,
                products.c.name,
                products.c.price,
                products.c.stock,
                products.c.number_of_purchases
            )
            result = await conn.execute(stmt)
            rows = result.fetchall()
            return [
                {
                    "id": r.id,
                    "name": r.name,
                    "price": r.price,
                    "stock": r.stock,
                    "number_of_purchases": r.number_of_purchases
                }
                for r in rows
            ]

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def get_product_by_id(product_id: int) -> Optional[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = select(
                products.c.id,
                products.c.name,
                products.c.price,
                products.c.stock,
                products.c.number_of_purchases
            ).where(products.c.id == product_id)
            result = await conn.execute(stmt)
            row = result.fetchone()
            if row:
                return {"id": row.id,
                        "name": row.name,
                        "price": row.price,
                        "stock": row.stock,
                        "number_of_purchases": row.number_of_purchases}
            return None

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def update_product_by_id(product_id: int, **kwargs) -> Optional[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            update_data = {
                key: value for key, value in kwargs.items()
                if value is not None and key in PRODUCT_FIELDS
            }

            if not update_data:
                return None

            stmt = (
                update(products)
                .where(products.c.id == product_id)
                .values(**update_data)
                .returning(
                    products.c.id,
                    products.c.name,
                    products.c.price,
                    products.c.stock,
                    products.c.number_of_purchases
                )
            )
            result = await conn.execute(stmt)
            await conn.commit()
            row = result.fetchone()
            if row:
                return {"id": row.id,
                        "name": row.name,
                        "price": row.price,
                        "stock": row.stock,
                        "number_of_purchases": row.number_of_purchases}
            return None

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e


async def delete_product_by_id(product_id: int) -> Optional[Dict]:
    assert engine is not None, "Call init_database() first"
    async with engine.connect() as conn:
        try:
            stmt = (
                delete(products)
                .where(products.c.id == product_id)
                .returning(
                    products.c.id,
                    products.c.name,
                    products.c.price,
                    products.c.stock,
                    products.c.number_of_purchases
                )
            )
            result = await conn.execute(stmt)
            await conn.commit()
            row = result.fetchone()
            if row:
                return {"id": row.id,
                        "name": row.name,
                        "price": row.price,
                        "stock": row.stock,
                        "number_of_purchases": row.number_of_purchases}
            return None

        except SQLAlchemyError as e:
            await conn.rollback()
            raise e