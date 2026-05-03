import time
import hmac
import hashlib
import requests
from urllib.parse import urlencode
from bot.logging_config import setup_logger

logger = setup_logger("binance_client")
BASE_URL = "https://demo-fapi.binance.com"

class BinanceClient:
    def __init__(self, api_key, api_secret):
        self.api_key = api_key
        self.api_secret = api_secret
        self.session = requests.Session()
        self.session.headers.update({
            "X-MBX-APIKEY": self.api_key,
            "Content-Type": "application/json"
        })
        logger.info("BinanceClient initialized")

    def _timestamp(self):
        return int(time.time()*1000)-2000

    def _sign(self, params):
        query_string = urlencode(params)
        return hmac.new(self.api_secret.encode("utf-8"), query_string.encode("utf-8"), hashlib.sha256).hexdigest()

    def _get(self, endpoint, params=None, signed=False):
        params = params or {}
        if signed:
            params["timestamp"] = self._timestamp()
            params["signature"] = self._sign(params)
        url = BASE_URL + endpoint
        resp = self.session.get(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def _post(self, endpoint, params):
        params["timestamp"] = self._timestamp()
        params["signature"] = self._sign(params)
        url = BASE_URL + endpoint
        resp = self.session.post(url, params=params, timeout=10)
        resp.raise_for_status()
        return resp.json()

    def ping(self):
        try:
            self._get("/fapi/v1/ping")
            return True
        except Exception:
            return False

    def get_account_info(self):
        return self._get("/fapi/v2/account", signed=True)

    def place_order(self, symbol, side, order_type, quantity, price=None, time_in_force="GTC"):
        params = {"symbol": symbol.upper(), "side": side.upper(), "type": order_type.upper(), "quantity": quantity}
        if order_type.upper() == "LIMIT":
            if price is None:
                raise ValueError("Price required for LIMIT orders.")
            params["price"] = price
            params["timeInForce"] = time_in_force
        return self._post("/fapi/v1/order", params)
