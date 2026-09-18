import requests
import sys
from pathlib import Path
import argparse

CLIENT_DIR = Path(__file__).resolve().parent.parent / "client"
if str(CLIENT_DIR) not in sys.path:
    sys.path.insert(0, str(CLIENT_DIR))

from client_api import APIClient

BASE_URL = "http://localhost:5000"


def test_users(client: APIClient) -> bool:
    created_user_id = None
    try:
        print("\n[1/6] Checking server...")
        check_server = client.check_server()
        assert check_server["status"] == "ok", "Server: invalid status"
        print(f"OK: {check_server}")

        print("\n[2/6] Getting all users...")
        users = client.get_all_users()
        assert isinstance(users, list), "User: response must be a list"
        print(f"Number of users found: {len(users)}")

        print("\n[3/6] Creating a test user...")
        created = client.create_user("Test User", "test@example.ru", 99)
        created_user_id = created["id"]
        assert created["name"] == "Test User", "User: error on creation"
        print(f"User created: ID={created_user_id}")

        print("\n[4/6] Getting a user by ID...")
        found = client.get_user_by_id(created_user_id)
        assert found and found["id"] == created_user_id, "User: not found"
        print(f"User found: {found}")

        print("\n[5/6] User update...")
        updated = client.update_user_by_id(created_user_id, age=100)
        assert updated and updated["age"] == 100, "User: age not updated"
        print("User age updated: 100")

        print("\n[6/6] User delete...")
        deleted = client.delete_user_by_id(created_user_id)
        created_user_id = None
        assert deleted and deleted["id"] == created["id"], "User: has not been deleted"
        print(f"User deleted: ID={deleted['id']}")

        print("\n" + "=" * 30)
        print("USERS: OK")
        print("=" * 30)
        return True

    except AssertionError as error:
        print(f"\nERROR: {error}")
        return False
    except requests.exceptions.ConnectionError:
        print("\nERROR: Failed to connect to the server")
        return False
    except requests.RequestException as error:
        print(f"\nERROR HTTP: {error}")
        return False
    finally:
        if created_user_id is not None:
            try:
                client.delete_user_by_id(created_user_id)
                print(f"\nCleanup: test user ID={created_user_id} deleted")
            except requests.RequestException:
                print(f"\nWarning: Failed to delete test user ID={created_user_id}")


def test_products(client: APIClient) -> bool:
    created_product_id = None
    try:
        print("\n[1/6] Checking server...")
        check_server = client.check_server()
        assert check_server["status"] == "ok", "Server: invalid status"
        print(f"OK: {check_server}")

        print("\n[2/6] Getting all products...")
        products = client.get_all_products()
        assert isinstance(products, list), "Product: response must be a list"
        print(f"Number of products found: {len(products)}")

        print("\n[3/6] Creating a test product...")
        created = client.create_product("Test Product", 123, 22, 11)
        created_product_id = created["id"]
        assert created["name"] == "Test Product", "Product: error on creation"
        print(f"Product created: ID={created_product_id}")

        print("\n[4/6] Getting a product by ID...")
        found = client.get_product_by_id(created_product_id)
        assert found and found["id"] == created_product_id, "Product: not found"
        print(f"Product found: {found}")

        print("\n[5/6] Product update...")
        updated = client.update_product_by_id(created_product_id, stock=999)
        assert updated and updated["stock"] == 999, "Product: stock not updated"
        print("Product stock updated: 999")

        print("\n[6/6] Product delete...")
        deleted = client.delete_product_by_id(created_product_id)
        created_product_id = None
        assert deleted and deleted["id"] == created["id"], "Product: has not been deleted"
        print(f"Product deleted: ID={deleted['id']}")

        print("\n" + "=" * 30)
        print("PRODUCTS: OK")
        print("=" * 30)
        return True

    except AssertionError as error:
        print(f"\nERROR: {error}")
        return False
    except requests.exceptions.ConnectionError:
        print("\nERROR: Failed to connect to the server")
        return False
    except requests.RequestException as error:
        print(f"\nERROR HTTP: {error}")
        return False
    finally:
        if created_product_id is not None:
            try:
                client.delete_product_by_id(created_product_id)
                print(f"\nCleanup: test product ID={created_product_id} deleted")
            except requests.RequestException:
                print(f"\nWarning: Failed to delete test product ID={created_product_id}")


def run_autotest(base_url: str = BASE_URL) -> bool:
    client = APIClient(base_url)

    print("\n" + "=" * 30)
    print("Starting the autotest")
    print("=" * 30)

    pass_users = test_users(client)
    pass_products = test_products(client)

    if pass_users and pass_products:
        print("\n" + "=" * 30)
        print("ALL: OK")
        print("=" * 30)

    return pass_users and pass_products


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSON Database API Autotest")
    parser.add_argument("--url", default=BASE_URL, 
                        help="Server URL (default: http://127.0.0.1:5000)")

    args = parser.parse_args()

    run_autotest(args.url)