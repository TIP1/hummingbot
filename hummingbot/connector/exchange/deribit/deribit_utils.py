from decimal import Decimal
from typing import Any, Dict

from hummingbot.client.config.config_methods import using_exchange
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.core.data_type.trade_fee import TradeFeeSchema

CENTRALIZED = True
EXAMPLE_PAIR = "ZRX-ETH"

DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("0.001"),
    taker_percent_fee_decimal=Decimal("0.001"),
    buy_percent_fee_deducted_from_returns=True
)


def is_exchange_information_valid(exchange_info: Dict[str, Any]) -> bool:
    """
    Verifies if a trading pair is enabled to operate with based on its exchange information
    :param exchange_info: the exchange information for a trading pair
    :return: True if the trading pair is enabled, False otherwise
    """
    return exchange_info.get("status", None) == "TRADING" and "SPOT" in exchange_info.get("permissions", list())


KEYS = {
    "deribit_api_key":
        ConfigVar(key="deribit_api_key",
                  prompt="Enter your Deribit API key >>> ",
                  required_if=using_exchange("deribit"),
                  is_secure=True,
                  is_connect_key=True),
    "deribit_api_secret":
        ConfigVar(key="deribit_api_secret",
                  prompt="Enter your Deribit API secret >>> ",
                  required_if=using_exchange("deribit"),
                  is_secure=True,
                  is_connect_key=True),
}

OTHER_DOMAINS = ["deribit_us"]
OTHER_DOMAINS_PARAMETER = {"deribit_us": "us"}
OTHER_DOMAINS_EXAMPLE_PAIR = {"deribit_us": "BTC-USDT"}
OTHER_DOMAINS_DEFAULT_FEES = {"deribit_us": [0.1, 0.1]}
OTHER_DOMAINS_KEYS = {"deribit_us": {
    "deribit_us_api_key":
        ConfigVar(key="deribit_us_api_key",
                  prompt="Enter your Deribit US API key >>> ",
                  required_if=using_exchange("deribit_us"),
                  is_secure=True,
                  is_connect_key=True),
    "deribit_us_api_secret":
        ConfigVar(key="deribit_us_api_secret",
                  prompt="Enter your Deribit US API secret >>> ",
                  required_if=using_exchange("deribit_us"),
                  is_secure=True,
                  is_connect_key=True),
}}
