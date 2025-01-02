import MetaTrader5 as mt5
import time
import logging
from modules.data_manager import RealTimeDataManager

def initialize_mt5():
    """Initialize MetaTrader 5 connection."""
    if not mt5.initialize():
        logging.error("MetaTrader 5 initialization failed")
        return False
    return True

def shutdown_mt5():
    """Shutdown MetaTrader 5 connection."""
    mt5.shutdown()

def place_mt5_trade(symbol, lot_size, order_type):
    """Place a trade using MetaTrader 5."""
    symbol_info = mt5.symbol_info(symbol)
    if not symbol_info:
        logging.error(f"Symbol {symbol} not found")
        return

    # Ensure the symbol is selected
    if not symbol_info.visible:
        if not mt5.symbol_select(symbol, True):
            logging.error(f"Failed to select symbol {symbol}")
            return

    price = mt5.symbol_info_tick(symbol).ask if order_type == "buy" else mt5.symbol_info_tick(symbol).bid
    trade_request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": symbol,
        "volume": lot_size,
        "type": mt5.ORDER_BUY if order_type == "buy" else mt5.ORDER_SELL,
        "price": price,
        "deviation": 10,
        "magic": 123456,
        "comment": "Python Trade",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(trade_request)
    if result.retcode != mt5.TRADE_RETCODE_DONE:
        logging.error(f"Trade failed: {result}")
    else:
        logging.info(f"Trade successful: {result}")

def calculate_rule_signal(data):
    """
    Generate a rule-based signal using technical indicators like RSI and MACD.
    """
    try:
        # Placeholder calculations for RSI and MACD
        rsi = 50  # Replace with actual RSI calculation logic
        macd = 0  # Replace with actual MACD calculation logic

        signal = 0
        if rsi < 30:
            signal += 0.5
        elif rsi > 70:
            signal -= 0.5

        if macd > 0:
            signal += 0.5
        elif macd < 0:
            signal -= 0.5

        return max(-1, min(1, signal))
    except Exception as e:
        logging.error(f"Error calculating rule signal: {e}")
        return 0

def real_time_decision_pipeline(symbol, lot_size):
    """
    Real-time trading logic using MetaTrader 5 integration.
    """
    if not initialize_mt5():
        return

    data_manager = RealTimeDataManager()
    while True:
        try:
            tick_data = data_manager.fetch_tick_data(symbol)
            processed_data = data_manager.calculate_custom_indicators(tick_data)
            decision_signal = calculate_rule_signal(processed_data)

            if decision_signal > 0.5:
                place_mt5_trade(symbol, lot_size, "buy")
            elif decision_signal < -0.5:
                place_mt5_trade(symbol, lot_size, "sell")

            time.sleep(0.05)
        except Exception as e:
            logging.error(f"Error in trading loop: {e}")

    shutdown_mt5()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    real_time_decision_pipeline("EURUSD", 0.1)
