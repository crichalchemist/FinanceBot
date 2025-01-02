import logging
import time

from modules.data_manager import RealTimeDataManager
from modules.model_manager import OptimizedModelManager
from modules.track_performanceDB import track_performance
from modules.trade_manager import FastTradeManager



def real_time_decision_pipeline(symbol, volume):
    """
    Real-time trading decision pipeline prioritizing ML insights.
    """
    # Configuration
    ml_confidence_threshold = 0.5
    fallback_threshold = 0.3

    # Initialize components
    data_manager = RealTimeDataManager()
    model_manager = OptimizedModelManager()
    trade_manager = FastTradeManager()

    while True:
        try:
            # Fetch and process market data
            tick_data = data_manager.fetch_tick_data(symbol)
            processed_data = data_manager.calculate_custom_indicators(tick_data)
            features = processed_data[['mid_price', 'spread', 'momentum']].to_dict('records')[0]

            # ML prediction
            ml_prediction = model_manager.predict([[features['mid_price'], features['spread'], features['momentum']]])[0]

            # Fallback to rules-based signal
            rule_signal = calculate_rule_signal(processed_data)

            # Prioritize ML, use rules as fallback
            if abs(ml_prediction) >= ml_confidence_threshold:
                decision_signal = ml_prediction
                decision_source = "ML"
            elif abs(rule_signal) >= fallback_threshold:
                decision_signal = rule_signal
                decision_source = "Rules"
            else:
                decision_signal = 0
                decision_source = "None"

            # Execute trades and log performance
            if decision_signal > 0.5:
                trade_manager.place_trade(symbol, volume, "buy")
                trade_outcome = "profit"  # Placeholder for outcome
            elif decision_signal < -0.5:
                trade_manager.place_trade(symbol, volume, "sell")
                trade_outcome = "profit"  # Placeholder for outcome
            else:
                trade_outcome = "no_trade"

            # Track performance
            track_performance(decision_source, decision_signal, trade_outcome)

            # Sleep for loop efficiency
            time.sleep(0.05)
        except Exception as e:
            logging.error(f"Error in decision pipeline: {e}")


# Exportable for external imports
__all__ = ["real_time_decision_pipeline"]
