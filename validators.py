from typing import Optional

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}

class ValidationError(Exception):
    pass

def validate_symbol(symbol):
    symbol = symbol.strip().upper()
    if not symbol:
        raise ValidationError("Symbol cannot be empty.")
    return symbol

def validate_side(side):
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'.")
    return side

def validate_order_type(order_type):
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(f"Invalid type '{order_type}'.")
    return order_type

def validate_quantity(quantity_str):
    try:
        qty = float(quantity_str)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid quantity '{quantity_str}'.")
    if qty <= 0:
        raise ValidationError("Quantity must be greater than 0.")
    return qty

def validate_price(price_str, order_type):
    if order_type.upper() == "MARKET":
        return None
    if not price_str:
        raise ValidationError("Price required for LIMIT orders.")
    try:
        price = float(price_str)
    except (ValueError, TypeError):
        raise ValidationError(f"Invalid price '{price_str}'.")
    if price <= 0:
        raise ValidationError("Price must be greater than 0.")
    return price

def validate_all(symbol, side, order_type, quantity, price=None):
    symbol = validate_symbol(symbol)
    side = validate_side(side)
    order_type = validate_order_type(order_type)
    qty = validate_quantity(quantity)
    prc = validate_price(price, order_type)
    return symbol, side, order_type, qty, prc