from typing import Dict, Optional

from hummingbot.core.data_type.common import TradeType
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_message import OrderBookMessage, OrderBookMessageType

from .deribit_constants import SIDE_BUY, SIDE_SELL


class DeribitOrderBook(OrderBook):

    @classmethod
    def snapshot_message_from_exchange(cls,
                                       msg: Dict[str, any],
                                       timestamp: float,
                                       metadata: Optional[Dict] = None) -> OrderBookMessage:
        """
        Creates a snapshot message with the order book snapshot message
        :param msg: the response from the exchange when requesting the order book snapshot
        :param timestamp: the snapshot timestamp
        :param metadata: a dictionary with extra information to add to the snapshot data
        :return: a snapshot message with the snapshot information received from the exchange
        """
        if metadata:
            msg.update(metadata)
        # ToDo: https://docs.deribit.com/?python#public-get_order_book
        return OrderBookMessage(OrderBookMessageType.SNAPSHOT, {
            "trading_pair": msg["instrument_name"],
            "update_id": msg["change_id"],
            "bids": msg["bids"],
            "asks": msg["asks"]
        }, timestamp=timestamp)

    @classmethod
    def diff_message_from_exchange(cls,
                                   msg: Dict[str, any],
                                   timestamp: Optional[float] = None,
                                   metadata: Optional[Dict] = None) -> OrderBookMessage:
        """
        Creates a diff message with the changes in the order book received from the exchange
        :param msg: the changes in the order book
        :param timestamp: the timestamp of the difference
        :param metadata: a dictionary with extra information to add to the difference data
        :return: a diff message with the changes in the order book notified by the exchange
        """
        if metadata:
            msg.update(metadata)
        return OrderBookMessage(OrderBookMessageType.DIFF, {
            "trading_pair": msg["instrument_name"],
            "first_update_id": msg["prev_change_id"],
            "update_id": msg["change_id"],
            "bids": msg["bids"],
            "asks": msg["asks"]
        }, timestamp=timestamp)

    @classmethod
    def trade_message_from_exchange(cls, msg: Dict[str, any], metadata: Optional[Dict] = None):
        """
        Creates a trade message with the information from the trade event sent by the exchange
        :param msg: the trade event details sent by the exchange
        :param metadata: a dictionary with extra information to add to trade message
        :return: a trade message with the details of the trade as provided by the exchange
        """
        if metadata:
            msg.update(metadata)
        
        if msg["direction"] == SIDE_SELL:
            trade_type = float(TradeType.SELL.value)
        elif msg["direction"] == SIDE_BUY:
            trade_type = float(TradeType.BUY.value)
        else:
            raise ValueError(f"Unexpected trade type: {msg['direction']}")

        return OrderBookMessage(OrderBookMessageType.TRADE, {
            "trading_pair": msg["instrument_name"],
            "trade_type": trade_type,
            "trade_id": msg["trade_id"],
            "update_id": msg["timestamp"],
            "price": msg["price"],
            "amount": msg["amount"]
        }, timestamp=msg["timestamp"] * 1e-3)
