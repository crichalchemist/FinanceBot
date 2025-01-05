import logging
import time

from data_manager import RealTimeDataManager
from data_uploader import DataUploader
from model_manager import OptimizedModelManager
from trade_manager import FastTradeManager


def combined_decision_pipeline(symbol, volume, api_url):
    """
    Real-time pipeline for making trade decisions.
    Combines machine learning predictions, rules-based signals, and external API validation.
    """
    # Initialize components
    data_manager = RealTimeDataManager()
    model_manager = OptimizedModelManager()
    trade_manager = FastTradeManager()
    uploader = DataUploader(api_url)

    while True:
        try:
            # Step 1: Fetch and Process Data
            tick_data = data_manager.fetch_tick_data(symbol)
            processed_data = data_manager.calculate_custom_indicators(tick_data)
            features = processed_data[['mid_price', 'spread', 'momentum']].to_dict('records')[0]

            # Step 2: Machine Learning Prediction
            ml_prediction = model_manager.predict([[features['mid_price'], features['spread'], features['momentum']]])[0]

            # Step 3: Rules-Based Signal
            rule_signal = calculate_rule_signal(processed_data)

            # Step 4: Combine Signals
            combined_signal = (0.6 * ml_prediction) + (0.4 * rule_signal)

            # Step 5: Execute Trades Based on Combined Signal
            decision = None
            if combined_signal > 0.5:
                trade_manager.place_trade(symbol, volume, "buy")
                decision = "buy"
            elif combined_signal < -0.5:
                trade_manager.place_trade(symbol, volume, "sell")
                decision = "sell"

            # Step 6: Send Data for Analysis
            trade_data = {
                "symbol": symbol,
                "features": features,
                "ml_prediction": ml_prediction,
                "rule_signal": rule_signal,
                "combined_signal": combined_signal,
                "decision": decision,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")
            }
            uploader.send_trade_data(trade_data)

            # Sleep to ensure loop efficiency (limit CPU usage)
            time.sleep(0.05)  # ~50ms to ensure 80ms total time
        except Exception as e:
            logging.error(f"Error in combined decision pipeline: {e}")
