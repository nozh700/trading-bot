from typing import Optional
from bot.client import BinanceClient
from bot.validators import validate_all, ValidationError
from bot.logging_config import setup_logger

logger= setup_logger("orders")

def print_order_summary(symbol, side, order_type, quantity, price):
    print("\n"+"="*52)
    print("          ORDER REQUEST SUMMARY")
    print("="*52)
    print(f"  Symbol  : {symbol}")
    print(f"  Side    : {side}")
    print(f"   Type   : {order_type}")
    print(f"    Quantity  : {quantity}")
    if price:
        print(f"   Price   :{price}")
    print("="*52)



def print_order_response(response):
    print("\n"+"="*52)
    print("     ORDER REQUEST SUMMARY")
    print("-"*52)
    print(f"  Order ID  :{response.get('orderId','N/A')}")
    print(f"  Status  :{response.get('status','N/A')}")
    print(f"  Symbol  :{response.get('symbol','N/A')}")
    print(f"  Side  :{response.get('side','N/A')}")
    print(f"  Type  :{response.get('type','N/A')}")
    print(f"  Orig Qty  :{response.get('origQty','N/A')}")
    print(f"Executed Qty  :{response.get('executedQty','N/A')}")
    avg=response.get('avgPrice','0')
    print(f"  Avg Price  :{avg if float(avg or 0)>0 else 'N/A'}")
    print(f"  TimeInForce  :{response.get('timeInForce'),'N/A'}")
    print("="*52)

def place_order(client, symbol,side, order_type, quantity,price=None):
    logger.info(
        f"Order request | symbol={symbol} side={side}"
        f"type={order_type} qty={quantity} price={price}"
    )
    try:
        sym,s,ot,qty,prc=validate_all(
            symbol,side,order_type,quantity,price
        )
    except Exception as e:
        logger.warning(f"Validation failed:{e}")
        raise
    print_order_summary(sym,s,ot,qty,prc)

    try:
        response=client.place_order(
            symbol=sym, side=s, order_type=ot,
            quantity=qty, price=prc
        )    
    except Exception as e:
        logger.error(f"Order failed:{e}")
        raise

    print_order_response(response)
    print("\n Order placed successfully!\n")
    logger.info(
        f"Order success | orderId={response.get('orderId')}"
        f"status={response.get('status')}"
    )    
    return response


            
