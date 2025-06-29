from flask import Flask, request, jsonify
from flask_cors import CORS
from pricer import (call_option, put_option)
from heatmap import (call_option_heatmap, put_option_heatmap)
from greeks import get_greeks

app = Flask(__name__)
CORS(app)

@app.route('/api/call-price', methods=['POST'])
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
    

@app.route('/api/put-price', methods=['POST'])
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
    

@app.route('/api/call-heatmap', methods=['POST'])
def get_call_heatmap():
    data = request.get_json()
    try:
        result = call_option_heatmap(
            ticker=data['ticker'],
            option_vol=data['option_vol'],
            period_vol=data['period_vol'],
        )
        return jsonify({'heatmap' : result})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    

@app.route('/api/put-heatmap', methods=['POST'])
def get_put_heatmap():
    data = request.get_json()
    try:
        result = put_option_heatmap(
            ticker=data['ticker'],
            option_vol=data['option_vol'],
            period_vol=data['period_vol']
        )
        return jsonify({'heatmap' : result})
    except Exception as e:
        return jsonify({'error' : str(e)}), 500
    

@app.route('/api/get-greeks', methods=["POST"])
def get_greek_symbols():
    data = request.get_json()
    try:
        result = get_greeks(
            opt_type=data['opt_type'],
            ticker=data['ticker'],
            strike_price=data['strike_price'],
            option_vol=data['option_vol'],
            period_vol=data['period_vol'],
            period_opt=data['period_opt'],
            output=data['output']
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({'error' : str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=8000)