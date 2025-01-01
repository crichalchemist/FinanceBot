from flask import Flask, request, jsonify
from modules.data_manager import RealTimeDataManager
from modules.trade_manager import FastTradeManager
from modules.analysis_server import analyze_trade_data
import logging

app = Flask(__name__)

data_manager = RealTimeDataManager()
trade_manager = FastTradeManager()

@app.route('/data', methods=['GET'])
def get_data():
    symbol = request.args.get('symbol')
    max_ticks = int(request.args.get('max_ticks', 1000))
    try:
        data = data_manager.fetch_tick_data(symbol, max_ticks)
        return data.to_json(), 200
    except Exception as e:
        logging.error(f"Error fetching data: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/trade', methods=['POST'])
def trade():
    data = request.json
    try:
        result = trade_manager.place_trade(data['symbol'], data['volume'], data['direction'])
        return jsonify({"success": result.retcode == mt5.TRADE_RETCODE_DONE}), 200
    except Exception as e:
        logging.error(f"Error placing trade: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/analyze', methods=['GET'])
def analyze():
    try:
        return jsonify(analyze_trade_data()), 200
    except Exception as e:
        logging.error(f"Error analyzing trades: {e}")
        return jsonify({"error": str(e)}), 500
