import re
from typing import List, Dict, Any, Tuple, Optional, Callable


USER_VALIDATORS = {
    "name": lambda a: validate_name(a),
    "email": lambda a: validate_email(a),
    "age": lambda a: validate_age(a),
}


PRODUCT_VALIDATORS = {
    "name": lambda a: validate_name(a),
    "price": lambda a: validate_price(a),
    "stock": lambda a: validate_stock(a),
    "number_of_purchases": lambda a: validate_number_of_purchases(a),
}


def validate_name(name: str) -> Tuple[bool, Optional[str], Optional[str]]:
    if not name or not name.strip():
        return False, None, "Error: Name cannot be empty"
    if len(name.strip()) > 100:
        return False, None, "Error: Name must be less than 100 characters"
    return True, name, None


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    if not email:
        return False, None, "Error: Email cannot be empty"
    if "@" not in email:
        return False, None, "Error: Email must contain @"
    if len(email) < 5:
        return False, "Error: Email must contain at least 5 characters"
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        return False, "Error: Invalid email format (example: user@example.com)"
    return True, email, None


def validate_price(price_str: str) -> Tuple[bool, Optional[float], Optional[str]]:
    try:
        price = float(price_str)
        if price < 0 or price > 1_000_000:
            return False, None, "Error: Price cannot be negative or greater than 1_000_000"
        return True, price, None
    except ValueError:
        return False, None, "Error: Price must be a number (example: 99.99)"


def validate_age(age_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    try:
        age = int(age_str)
        if age < 1 or age > 200:
            return False, None, "Error: Age must be between 1 and 200"
        return True, age, None
    except ValueError:
        return False, None, "Error: Age must be an integer (example: 22)"


def validate_stock(stock_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    try:
        if "." in stock_str:
            return False, None, "Error: Stock must be an integer (example: 50)"
        stock = int(stock_str)
        if stock < 0 or stock > 1_000_000:
            return False, None, "Error: Stock cannot be negative or greater than 1_000_000"
        return True, stock, None
    except ValueError:
        return False, None, "Error: Stock must be an integer (example: 50)"


def validate_number_of_purchases(number_of_purchases: str) -> Tuple[bool, Optional[int], Optional[str]]:
    return validate_stock(number_of_purchases)


Validator = Callable[[str], Tuple[bool, Optional[Any], Optional[str]]]


def collect_quoted_args(args: List[str]) -> List[str]:
    result, buffer = [], []

    for arg in args:
        if buffer or arg.startswith('"'):
            buffer.append(arg)
            if arg.endswith('"') and len(buffer) > 0:
                result.append(" ".join(buffer))
                buffer = []
        else:
            result.append(arg)

    return result + ([" ".join(buffer)] if buffer else [])


def extract_quoted_name(args: List[str]) -> Tuple[Optional[str], List[str], Optional[str]]:
    args = collect_quoted_args(args)
    print(f"DEBUG extract_quoted_name: args = {args}")
    if not args:
        return None, [], "Error in name: No arguments provided"

    name_arg = args[0]
    if not (name_arg.startswith('"') and name_arg.endswith('"')):
        return None, args, "Error in name: Must be in quotes (example: \"User Name\")"
    name = name_arg[1:-1]
    if not name.strip():
        return None, args, "Error in name: Cannot be empty"

    return name, args[1:], None


def parse_create(args: List[str], validators: Dict[str, Validator],
                 optional_fields: Optional[List[str]] = None
                 ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    optional_fields = optional_fields or []
    result = {}
    keys = list(validators.keys())

    if keys and keys[0] == "name":
        name, remaining_args, error = extract_quoted_name(args)
        if error:
            return None, error

        ok, parsed, error = validators["name"](name)
        if not ok:
            return None, f"Error in name: {error}"
        result["name"] = parsed

        args = remaining_args
        keys = [k for k in keys if k != "name"]

    for i, key in enumerate(keys):
        if i < len(args):
            value = args[i]
        elif key in optional_fields:
            continue
        else:
            return None, f"Error: Required field is missing '{key}'"

        validation_result = validators[key](value)

        if len(validation_result) == 3:
            ok, parsed, error = validation_result
        elif len(validation_result) == 2:
            ok, error = validation_result
            parsed = value if ok else None
        else:
            return None, f"Error: Invalid validation result for {key}"

        if not ok:
            return None, f"Error in {key}: {error}"
        result[key] = parsed

    return result, None


def parse_update(args: List[str], validators: Dict[str, Validator]
                 ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    updates = {}
    current_key = None
    current_value = []
    for arg in args:
        if "=" in arg:
            if current_key:
                value = " ".join(current_value)
                ok, parsed, error = validators[current_key](value)
                if not ok:
                    return None, f"Error in {current_key}: {error}"
                updates[current_key] = parsed

            key, value = arg.split("=", 1)
            current_key = key.strip()
            current_value = [value.strip()] if value.strip() else []
        else:
            if current_key is None:
                return None, f"Invalid format: '{arg}'. Expected 'field=value'"
            current_value.append(arg)

    if current_key:
        value = " ".join(current_value)
        ok, parsed, error = validators[current_key](value)
        if not ok:
            return None, f"Error in {current_key}: {error}"
        updates[current_key] = parsed

    return updates, None


def parse_and_validate(args: List[str], validators: Dict[str, Validator],
                       mode: str, optional_fields: Optional[List[str]] = None
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if mode == "update":
        return parse_update(args, validators)
    elif mode == "create":
        return parse_create(args, validators, optional_fields)
    else:
        return None, f"Unknown mode '{mode}'"