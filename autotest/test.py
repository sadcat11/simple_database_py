import requests
import sys
from pathlib import Path

CLIENT_DIR = Path(__file__).resolve().parent.parent / "client"
if str(CLIENT_DIR) not in sys.path:
    sys.path.insert(0, str(CLIENT_DIR))

from client_api import APIClient

BASE_URL = "http://localhost:5000"

from client_api import APIClient
def run_autotest(base_url: str = BASE_URL) -> bool:
    client = APIClient(base_url)
    created_user_id = None

    print("\n" + "=" * 30)
    print("Starting the autotest")
    print("=" * 30)

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
        print("ALL: OK")
        print("=" * 30)
        return True

    except AssertionError as error:
        print(f"\nFAIL: {error}")
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


if __name__ == "__main__":
    run_autotest()