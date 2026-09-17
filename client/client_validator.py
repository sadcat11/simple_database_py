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
}


def validate_name(name: str) -> Tuple[bool, Optional[str]]:
    if not name or not name.strip():
        return False, None, "Name cannot be empty"
    if len(name.strip()) > 100:
        return False, None, "Name must be less than 100 characters"
    return True, name, None


def validate_email(email: str) -> Tuple[bool, Optional[str]]:
    if not email:
        return False, None, "Email cannot be empty"
    if "@" not in email:
        return False, None, "Email must contain @"
    if len(email) < 5:
        return False, "Email must contain at least 5 characters"
    if not re.match(r"^[^@]+@[^@]+\.[^@]+$", email):
        return False, "Invalid email format (example: user@example.com)"
    return True, email, None


def validate_price(price_str: str) -> Tuple[bool, Optional[float], Optional[str]]:
    try:
        price = float(price_str)
        if price < 0 or price > 1_000_000:
            return False, None, "Price cannot be negative or greater than 1_000_000"
        return True, price, None
    except ValueError:
        return False, None, "Price must be a number (example: 99.99)"


def validate_age(age_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    try:
        age = int(age_str)
        if age < 1 or age > 200:
            return False, None, "Age must be between 1 and 200"
        return True, age, None
    except ValueError:
        return False, None, "Age must be an integer (example: 22)"


def validate_stock(stock_str: str) -> Tuple[bool, Optional[int], Optional[str]]:
    try:
        if "." in stock_str:
            return False, None, "Stock must be an integer (example: 50)"
        stock = int(stock_str)
        if stock < 0 or stock > 1_000_000:
            return False, None, "Stock cannot be negative or greater than 1_000_000"
        return True, stock, None
    except ValueError:
        return False, None, "Stock must be an integer (example: 50)"


Validator = Callable[[str], Tuple[bool, Optional[Any], Optional[str]]]

def parse_create(args: List[str], validators: Dict[str, Validator],
                 optional_fields: Optional[List[str]] = None
                 ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    optional_fields = optional_fields or []
    result = {}
    keys = list(validators.keys())
    
    for i, key in enumerate(keys):
        if i < len(args):
            value = args[i]
        elif key in optional_fields:
            value = "0"
        else:
            return None, f"Required field is missing '{key}'"
        
        validation_result = validators[key](value)
        
        if len(validation_result) == 3:
            ok, parsed, error = validation_result
        elif len(validation_result) == 2:
            ok, error = validation_result
            parsed = value if ok else None
        else:
            return None, f"Invalid validation result for {key}"
        
        if not ok:
            return None, f"Error in {key}: {error}"
        result[key] = parsed
    
    return result, None


def parse_update(args: List[str], validators: Dict[str, Validator]
                 ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    updates = {}
    for arg in args:
        if "=" not in arg:
            return None, f"Invalid format '{arg}' (field=value)"
        
        key, value = arg.split("=", 1)
        key = key.strip().lower()
        value = value.strip()
        
        if key not in validators:
            print(f"Unknown field '{key}'")
            updates[key] = value
            continue
        
        ok, parsed, error = validators[key](value)
        if not ok:
            return None, f"Error in {key}: {error}"
        updates[key] = parsed
    
    return updates, None


def parse_and_validate(args: List[str], validators: Dict[str, Validator],
                       mode: str, optional_fields: Optional[List[str]] = None,
) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    if mode == "update":
        return parse_update(args, validators)
    elif mode == "create":
        return parse_create(args, validators, optional_fields)
    else:
        return None, f"Unknown mode '{mode}'"