import logging

import MetaTrader5 as mt5


class FastTradeManager:
    def __init__(self):
        if not mt5.initialize():
            raise RuntimeError("Failed to initialize MetaTrader 5.")
        logging.info("FastTradeManager initialized.")

    def place_trade(self, symbol, volume, direction):
        """Place trades quickly."""
        order_type = mt5.ORDER_BUY if direction == "buy" else mt5.ORDER_SELL
        price = mt5.symbol_info_tick(symbol).ask if direction == "buy" else mt5.symbol_info_tick(symbol).bid

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
        }

        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logging.error(f"Trade failed: {result.comment}")
        else:
            logging.info(f"Trade placed successfully: {result}")
