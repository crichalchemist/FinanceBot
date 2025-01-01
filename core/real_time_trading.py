from modules.data_manager import RealTimeDataManager
from modules.trade_manager import FastTradeManager
import time
import logging

def real_time_trading(symbol, volume):
    data_manager = RealTimeDataManager()
    trade_manager = FastTradeManager()

    while True:
        try:
            tick_data = data_manager.fetch_tick_data(symbol)
            processed_data = data_manager.calculate_custom_indicators(tick_data)

            decision_signal = calculate_rule_signal(processed_data)

            if decision_signal > 0.5:
                trade_manager.place_trade(symbol, volume, "buy")
            elif decision_signal < -0.5:
                trade_manager.place_trade(symbol, volume, "sell")

            time.sleep(1)
        except Exception as e:
            logging.error(f"Error in trading loop: {e}")
