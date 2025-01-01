from data_manager import RealTimeDataManager
from model_manager import OptimizedModelManager
from trade_manager import FastTradeManager
import time
import logging

def calculate_rule_signal(data):
    """
    Calculate a rule-based signal from technical indicators (e.g., RSI, MACD).
    :param data: Processed data containing features and indicators.
    :return: Signal score (-1 to 1).
    """
    # Example logic for RSI and MACD (simplified)
    try:
        rsi = 50  # Placeholder for RSI calculation
        macd = 0  # Placeholder for MACD calculation

        signal = 0
        if rsi < 30:  # Oversold
            signal += 0.5
        elif rsi > 70:  # Overbought
            signal -= 0.5

        if macd > 0:  # Bullish momentum
            signal += 0.5
        elif macd < 0:  # Bearish momentum
            signal -= 0.5

        return max(-1, min(1, signal))  # Ensure signal is between -1 and 1
    except Exception as e:
        logging.error(f"Error calculating rule signal: {e}")
        return 0

def real_time_decision_pipeline(symbol, volume, api_url):
    """
    Real-time trading decision pipeline combining ML and rules-based logic.
    """
    # Initialize components
    data_manager = RealTimeDataManager()
    model_manager = OptimizedModelManager()
    trade_manager = FastTradeManager()

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
            combined_signal = (0.7 * ml_prediction) + (0.3 * rule_signal)

            # Step 5: Execute Trades
            if combined_signal > 0.5:
                trade_manager.place_trade(symbol, volume, "buy")
            elif combined_signal < -0.5:
                trade_manager.place_trade(symbol, volume, "sell")

            # Sleep for loop efficiency
            time.sleep(0.05)  # Adjust to ensure <80ms total time
        except Exception as e:
            logging.error(f"Error in real-time decision pipeline: {e}")
