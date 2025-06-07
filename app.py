from flask import Flask, request, jsonify
from backend.pricer import (call_option, put_option)
from backend.heatmap import (call_option_heatmap, put_option_heatmap)

app = Flask(__name__)

@app.route('api/call-price', methods=['POST'])
def get_call_price():
    data = request.get_json()
    try:
        result = call_option(
            ticker=data['ticker'],
            option_vol=data['option_vol'],
            period_vol=data['period_vol'],
            period_opt=data['period_opt'],
            strike_price=data['strike']
        )
        return jsonify({'price' : result})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    

@app.route('api/put-price', methods=['POST'])
def get_put_price():
    data = request.get_json()
    try:
        result = put_option(
            ticker=data['ticker'],
            option_vol=data['option_vol'],
            period_vol=data['period_vol'],
            period_opt=data['period_opt'],
            strike_price=data['strike']
        )
        return jsonify({'price' : result})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500