import argparse
import os
import sys
from dotenv import load_dotenv
from bot.client import BinanceClient
from bot.orders import place_order
from bot.validators import ValidationError
from bot.logging_config import setup_logger

logger = setup_logger("cli")

def load_credentials():
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY", "").strip()
    api_secret = os.getenv("BINANCE_API_SECRET", "").strip()
    if not api_key or not api_secret:
        print("ERROR: API credentials not found!")
        sys.exit(1)
    return api_key, api_secret

def cmd_ping(client, _args):
    if client.ping():
        print("Ping successful!")
    else:
        print("Ping failed")

def cmd_account(client, _args):
    try:
        info = client.get_account_info()
        print("Wallet:", info.get("totalWalletBalance"), "USDT")
    except Exception as e:
        print("Failed:", e)

def cmd_place(client, args):
    try:
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.type,
            quantity=args.quantity,
            price=args.price
        )
    except Exception as e:
        print("Order failed:", e)
        sys.exit(1)

def build_parser():
    parser = argparse.ArgumentParser(description="Trading Bot")
    sub = parser.add_subparsers(dest="command")
    sub.required = True
    sub.add_parser("ping")
    sub.add_parser("account")
    p = sub.add_parser("place")
    p.add_argument("--symbol", required=True)
    p.add_argument("--side", required=True, choices=["BUY","SELL"], type=str.upper)
    p.add_argument("--type", required=True, choices=["MARKET","LIMIT"], type=str.upper)
    p.add_argument("--quantity", required=True)
    p.add_argument("--price", default=None)
    return parser

def main():
    print("Binance Demo Trading Bot")
    api_key, api_secret = load_credentials()
    client = BinanceClient(api_key, api_secret)
    parser = build_parser()
    args = parser.parse_args()
    commands = {
        "ping": cmd_ping,
        "account": cmd_account,
        "place": cmd_place
    }
    commands[args.command](client, args)
if __name__ == "__main__":
    main()

