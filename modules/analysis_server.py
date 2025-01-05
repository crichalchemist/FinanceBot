import logging
import os

import pandas as pd
from flask import Flask, request, jsonify

app = Flask(__name__)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

# Path to save trade data
TRADE_DATA_PATH = "trade_data.csv"


@app.route('/api/trade_data', methods=['POST'])
def receive_trade_data():
    try:
        data = request.json
        logging.info(f"Received trade data: {data}")

        # Save data to CSV for analysis
        if os.path.exists(TRADE_DATA_PATH):
            df = pd.read_csv(TRADE_DATA_PATH)
        else:
            df = pd.DataFrame()

        df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)
        df.to_csv(TRADE_DATA_PATH, index=False)

        return jsonify({"status": "success"}), 200
    except Exception as e:
        logging.error(f"Error receiving trade data: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/api/analyze', methods=['GET'])
def analyze_trade_data():
    """Perform basic analysis on the trade data."""
    try:
        if not os.path.exists(TRADE_DATA_PATH):
            return jsonify({"error": "No trade data available"}), 404

        df = pd.read_csv(TRADE_DATA_PATH)
        analysis = {
            "total_trades": len(df),
            "profitable_trades": len(df[df["outcome"] == "profit"]),
            "accuracy": len(df[df["outcome"] == "profit"]) / len(df) if len(df) > 0 else 0,
        }

        return jsonify(analysis), 200
    except Exception as e:
        logging.error(f"Error analyzing trade data: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host= https://20.2.84.42, port=5001, debug=True)
