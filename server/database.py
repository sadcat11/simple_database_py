import json
import os
from dataclasses import dataclass
from typing import List, Dict, Optional

DB_FILE = "base.json"


@dataclass
class User:
    id: int
    name: str
    email: str
    age: int


@dataclass
class Product:
    id: int
    name: str
    price: float
    stock: int
    number_of_purchases: int


class Database:
    def __init__(self, db_file: str = DB_FILE):
        self.db_file = db_file
        if not os.path.exists(self.db_file):
            self._init_db()

# Initializing an empty database
    def _init_db(self):
        self._save({"users": [], "products": []})

# Loading data from JSON
    def _load(self) -> Dict[str, List]:
        if not os.path.exists(self.db_file):
            return {"users": [], "products": []}
        with open(self.db_file, "r", encoding="utf-8") as f:
            return json.load(f)

# Saving data to JSON
    def _save(self, data: Dict[str, List]):
        with open(self.db_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)


#===================
#====== USERS ======
#===================

    def create_user(self, name: str, email: str, age: int) -> Dict:
        data = self._load()
        max_id = max((u["id"] for u in data["users"]), default=0)
        new_user = {"id": max_id + 1, "name": name, "email": email, "age": age}
        data["users"].append(new_user)
        self._save(data)
        return new_user


    def get_all_users(self) -> List[Dict]:
        data = self._load()
        return data.get("users", [])


    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        users = self.get_all_users()
        for user in users:
            if user["id"] == user_id:
                return user
        return None


    def update_user_by_id(self, user_id: int, **kwargs) -> Optional[Dict]:
        data = self._load()
        for i, user in enumerate(data["users"]):
            if user["id"] == user_id:
                data["users"][i].update(kwargs)
                self._save(data)
                return data["users"][i]
        return None


    def delete_user_by_id(self, user_id: int) -> Optional[Dict]:
        data = self._load()
        for i, user in enumerate(data["users"]):
            if user["id"] == user_id:
                deleted = data["users"].pop(i)
                self._save(data)
                return deleted
        return None


#====================
#===== PRODUCTS =====
#====================

    def create_product(self, name: str, price: float, stock: int, number_of_purchases: int) -> Dict:
        data = self._load()
        max_id = max((p["id"] for p in data["products"]), default=0)
        new_product = {"id": max_id + 1, "name": name, "price": price,
                       "stock": stock, "number_of_purchases": number_of_purchases}
        data["products"].append(new_product)
        self._save(data)
        return new_product


    def get_all_products(self) -> List[Dict]:
        data = self._load()
        return data.get("products", [])


    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        products = self.get_all_products()
        for product in products:
            if product["id"] == product_id:
                return product
        return None


    def update_product_by_id(self, product_id: int, **kwargs) -> Optional[Dict]:
        data = self._load()
        for i, product in enumerate(data["products"]):
            if product["id"] == product_id:
                data["products"][i].update(kwargs)
                self._save(data)
                return data["products"][i]
        return None


    def delete_product_by_id(self, product_id: int) -> Optional[Dict]:
        data = self._load()
        for i, product in enumerate(data["products"]):
            if product["id"] == product_id:
                deleted = data["products"].pop(i)
                self._save(data)
                return deleted
        return None