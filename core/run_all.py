import multiprocessing
import logging
from real_time_trading import real_time_decision_pipeline
from modules.analysis_server import app as analysis_app
from train_model import train_model

def start_analysis_server():
    """Start the Flask-based analysis API server."""
    logging.info("Starting the analysis server...")
    analysis_app.run(host='0.0.0.0', port=5001, debug=False)

def start_decision_pipeline(symbol, volume, api_url):
    """Start the real-time decision pipeline."""
    logging.info(f"Starting the decision pipeline for {symbol}...")
    real_time_decision_pipeline(symbol=symbol, volume=volume, api_url=api_url)

def start_training_process():
    """Start the model training process."""
    logging.info("Starting the model training process...")
    train_model()

if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Configuration
    symbol = "EURUSD"
    volume = 0.1
    api_url = "http://localhost:5001/api/trade_data"

    # Create processes for analysis server, decision pipeline, and model training
    analysis_server_process = multiprocessing.Process(target=start_analysis_server)
    decision_pipeline_process = multiprocessing.Process(
        target=start_decision_pipeline,
        args=(symbol, volume, api_url)
    )
    training_process = multiprocessing.Process(target=start_training_process)

    # Start processes
    analysis_server_process.start()
    decision_pipeline_process.start()
    training_process.start()

    # Wait for processes to complete
    analysis_server_process.join()
    decision_pipeline_process.join()
    training_process.join()
