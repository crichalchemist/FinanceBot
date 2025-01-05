import logging
import time

import MetaTrader5 as mt5
import pandas as pd


class RealTimeDataManager:
    def __init__(self):
        if not mt5.initialize():
            raise RuntimeError("Failed to initialize MetaTrader 5.")
        logging.info("RealTimeDataManager initialized.")

    def fetch_tick_data(self, symbol, max_ticks=1000):
        """Fetch the latest tick data for the given symbol."""
        ticks = mt5.copy_ticks_from(symbol, time.time() - 60, max_ticks, mt5.COPY_TICKS_ALL)
        if ticks is None:
            raise ValueError(f"Failed to fetch tick data for {symbol}.")
        return pd.DataFrame(ticks)

    def calculate_custom_indicators(self, df):
        """Add custom indicators to tick data."""
        df['mid_price'] = (df['ask'] + df['bid']) / 2
        df['spread'] = df['ask'] - df['bid']
        df['momentum'] = df['mid_price'].diff()
        return df.tail(1)  # Keep only the latest processed row
