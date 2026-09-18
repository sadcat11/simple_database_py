import requests
from typing import List, Dict, Optional

BASE_URL = "http://localhost:5000"


class APIClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url.rstrip("/")


    def get_all_users(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/api/users")
        response.raise_for_status()
        return response.json()


    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        response = requests.get(f"{self.base_url}/api/users/{user_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


    def create_user(self, name: str, email: str = "", age: int = 0) -> Dict:
        response = requests.post(
            f"{self.base_url}/api/users",
            json={"name": name, "email": email, "age": age},
        )
        response.raise_for_status()
        return response.json()


    def update_user_by_id(self, user_id: int, **fields) -> Optional[Dict]:
        response = requests.put(
            f"{self.base_url}/api/users/{user_id}",
            json=fields,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


    def delete_user_by_id(self, user_id: int) -> Optional[Dict]:
        response = requests.delete(f"{self.base_url}/api/users/{user_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


    def get_all_products(self) -> List[Dict]:
        response = requests.get(f"{self.base_url}/api/products")
        response.raise_for_status()
        return response.json()


    def get_product_by_id(self, product_id: int) -> Optional[Dict]:
        response = requests.get(f"{self.base_url}/api/products/{product_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


    def create_product(self, name: str, price: float = 0.0,
                       stock: int = 0, number_of_purchases: int = 0) -> Dict:
        response = requests.post(
            f"{self.base_url}/api/products",
            json={"name": name, "price": price,
                  "stock": stock, "number_of_purchases": number_of_purchases},
        )
        response.raise_for_status()
        return response.json()


    def update_product_by_id(self, product_id: int, **fields) -> Optional[Dict]:
        response = requests.put(
            f"{self.base_url}/api/products/{product_id}",
            json=fields,
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


    def delete_product_by_id(self, product_id: int) -> Optional[Dict]:
        response = requests.delete(f"{self.base_url}/api/products/{product_id}")
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()


    def check_server(self) -> Dict:
        response = requests.get(f"{self.base_url}/api/check_server")
        response.raise_for_status()
        return response.json()