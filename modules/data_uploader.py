import logging

import requests


class DataUploader:
    def __init__(self, api_url):
        self.api_url = api_url

    def send_trade_data(self, data):
        """Send trade data to the analysis server."""
        try:
            response = requests.post(self.api_url, json=data)
            if response.status_code == 200:
                logging.info("Data uploaded successfully.")
            else:
                logging.error(f"Failed to upload data: {response.status_code}, {response.text}")
        except Exception as e:
            logging.error(f"Error uploading data: {e}")

# Usage Example
uploader = DataUploader(api_url="http://your-analysis-server/api/trade_data")
trade_data = {
    "symbol": "EURUSD",
    "features": {"mid_price": 1.1345, "momentum": 0.002},
    "ml_prediction": 0.8,
    "rule_signal": 0.4,
    "combined_signal": 0.7,
    "decision": "buy",
    "outcome": "profit",
    "timestamp": "2025-01-01T12:00:00"
}
uploader.send_trade_data(trade_data)
