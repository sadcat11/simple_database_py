import requests
from typing import List,  Dict, Optional, Any, Tuple
from client_api import APIClient
import argparse
from client_validator import *

BASE_URL = "http://localhost:5000"


#===================
#====== PRINT ======
#===================

def print_users(users: List[Dict]) -> None:
    if not users:
        print("There are no users in the database")
        return
    print(f"\nNumber of users in the database: {len(users)}")
    for user in users:
        print(f"[{user['id']}] {user['name']} <{user['email']}> (age: {user['age']})")


def print_user_by_id(user: Optional[Dict], user_id: int) -> None:
    if not user:
        print(f"User with ID={user_id} not found")
        return
    print(f"User {user_id}:")
    print(f"- Name: {user['name']}")
    print(f"- Email: {user['email']}")
    print(f"- Age: {user['age']}")


def print_products(products: List[Dict]) -> None:
    if not products:
        print("There are no products in the database")
        return
    print(f"\nNumber of products in the database: {len(products)}")
    for product in products:
        print(
f"""[{product['id']}] {product['name']}: {product['price']} $
    |(stock: {product['stock']}) Number of purchases: {product['number_of_purchases']}""")


def print_product_by_id(product: Optional[Dict], product_id: int) -> None:
    if not product:
        print(f"Product with ID={product_id} not found")
        return
    print(f"Product {product_id}:")
    print(f"- Name: {product['name']}")
    print(f"- Price: {product['price']} $")
    print(f"- Stock: {product['stock']}")
    print(f"- Number of purchases: {product['number_of_purchases']}")


def print_help() -> None:
    print("""
 _______________________________________________________________
|users                                 | show all users         |
|user <id>                             | show user with id      |
|create_user <"name"> <email> [age]    | create user            |
|update_user <id> <field>=<value>      | update user            |
|delete_user <id>                      | delete user            |
|______________________________________|________________________|
|products                              | show all products      |
|product <id>                          | show product with id   |
|create_product <"name"> <price>       | create product         |
|    <stock> [number_of_purchases]     |                        |
|update_product <id> <field>=<value>   | update product         |
|delete_product <id>                   | delete product         |
|______________________________________|________________________|
|help                                  | show command list      |
|exit                                  | exit                   |
|check_server                          | check server           |
|______________________________________|________________________|
""")

def print_banner(base_url: str) -> None:
    print(f"""
JSON DATABASE API CLIENT
Server: {base_url}
Input 'help' for a list of commands.
""")

#===================
#===== UTILITY =====
#===================

def parse_updates(args: List[str]) -> Dict[str, Any]:
    def convert(value: str) -> Any:
        if value.isdigit():
            return int(value)
        try:
            return float(value)
        except ValueError:
            return value

    pairs = (arg.split("=", 1) for arg in args if "=" in arg)
    return {key: convert(value) for key, value in pairs if key}


def parse_input(user_input: str) -> Tuple[str, List[str]]:
    parts = user_input.strip().split()
    return (parts[0].lower(), parts[1:]) if parts else ("", [])


def cmd_check_server(client: APIClient, args: List[str]) -> bool:
    result = client.check_server()
    print(f"Status: {result['status']}")
    print(f"Message: {result['message']}")
    return True


def cmd_help(client: APIClient, args: List[str]) -> bool:
    print_help()
    return True


def cmd_exit(client: APIClient, args: List[str]) -> bool:
    return True


#===================
#====== USERS ======
#===================

def cmd_create_user(client: APIClient, args: List[str]) -> bool:
    result, error = parse_and_validate(args, USER_VALIDATORS,
                                       mode="create",
                                       optional_fields=["age"])
    if error:
        print(f"Error: {error}")
        return False
    
    user = client.create_user(result["name"], result["email"], result.get("age", 0))
    print(f"User created: ID={user['id']}, {user['name']}")
    return True


def cmd_users(client: APIClient, args: List[str]) -> bool:
    print_users(client.get_all_users())
    return True


def cmd_user_by_id(client: APIClient, args: List[str]) -> bool:
    if not args:
        print("Error: Enter a user ID")
        return False
    user_id = int(args[0])
    print_user_by_id(client.get_user_by_id(user_id), user_id)
    return True


def cmd_update_user_by_id(client: APIClient, args: List[str]) -> bool:
    if len(args) < 2:
        print("Error: Specify ID and field in field=value format")
        return False

    try:
        user_id = int(args[0])
    except ValueError:
        print("Error: ID must be a number")
        return False
    
    result, error = parse_and_validate(args[1:], USER_VALIDATORS, mode="update")
    if error:
        print(f"Error: {error}")
        return False
    
    user = client.update_user_by_id(user_id, **result)
    print(f"Updated user: {user}" if user else f"User with ID={user_id} not found")
    return True


def cmd_delete_user_by_id(client: APIClient, args: List[str]) -> bool:
    if not args:
        print("Error: Enter a user ID")
        return False
    user_id = int(args[0])
    user = client.delete_user_by_id(user_id)
    print(f"User deleted: ID={user['id']}, {user['name']}" if user else f"User with ID={user_id} not found")
    return True


#====================
#===== PRODUCTS =====
#====================

def cmd_create_product(client: APIClient, args: List[str]) -> bool:
    result, error = parse_and_validate(args, PRODUCT_VALIDATORS,
                                       mode="create",
                                       optional_fields=["number_of_purchases"])
    if error:
        print(f"Error: {error}")
        return False
    
    product = client.create_product(result["name"], result["price"],
                                    result["stock"], result.get("number_of_purchases", 0))
    print(f"Product created: ID={product['id']}, {product['name']}")
    return True


def cmd_products(client: APIClient, args: List[str]) -> bool:
    print_products(client.get_all_products())
    return True


def cmd_product_by_id(client: APIClient, args: List[str]) -> bool:
    if not args:
        print("Error: Enter a product ID")
        return False
    product_id = int(args[0])
    print_product_by_id(client.get_product_by_id(product_id), product_id)
    return True


def cmd_update_product_by_id(client: APIClient, args: List[str]) -> bool:
    if len(args) < 2:
        print("Error: Specify ID and field in field=value format")
        return False

    try:
        product_id = int(args[0])
    except ValueError:
        print("Error: ID must be a number")
        return False

    result, error = parse_and_validate(args[1:], PRODUCT_VALIDATORS, mode="update")
    if error:
        print(f"Error: {error}")
        return False

    product = client.update_product_by_id(product_id, **result)
    print(f"Updated product: {product}" if product else f"Product with ID={product_id} not found")
    return True


def cmd_delete_product_by_id(client: APIClient, args: List[str]) -> bool:
    if not args:
        print("Error: Enter a product ID")
        return False
    product_id = int(args[0])
    product = client.delete_product_by_id(product_id)
    print(f"Product deleted: ID={product['id']}, {product['name']}" if product else f"Product with ID={product_id} not found")
    return True


COMMANDS = {
    "help": cmd_help,
    "check_server": cmd_check_server,
    "users": cmd_users,
    "user": cmd_user_by_id,
    "create_user": cmd_create_user,
    "update_user": cmd_update_user_by_id,
    "delete_user": cmd_delete_user_by_id,
    "products": cmd_products,
    "product": cmd_product_by_id,
    "create_product": cmd_create_product,
    "update_product": cmd_update_product_by_id,
    "delete_product": cmd_delete_product_by_id,
    "exit": cmd_exit,
}


def dispatch_command(client: APIClient, command: str, args: List[str]) -> bool:
    handler = COMMANDS.get(command)
    if handler is None:
        print(f"Unknown command: {command}. Type 'help' for a list of commands")
        return False
    return handler(client, args)


def interactive_console(base_url: str) -> None:
    client = APIClient(base_url)
    print_banner(base_url)
    while True:
        try:
            command, args = parse_input(input("\n>>> "))
            if command and not dispatch_command(client, command, args):
                print("Exit...")
                return
        except ValueError as error:
            print(f"Argument format error: {error}")
        except requests.exceptions.ConnectionError:
            print("Connection error:\nRun server or input correct URL \
                  'client.py --url <url>'")
        except KeyboardInterrupt:
            print("\nExit...")
            return
        except requests.RequestException as error:
            print(f"HTTP Error: {error}")


__all__ = [
    "cmd_create_user",
    "cmd_create_product",
    "cmd_update_user_by_id",
    "cmd_update_product_by_id",
]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="JSON Database API Client")
    parser.add_argument("--url", default=BASE_URL, 
                        help="Server URL (default: http://127.0.0.1:5000)")
    args = parser.parse_args()

    print(f"Connecting to {args.url}...")
    interactive_console(args.url)
