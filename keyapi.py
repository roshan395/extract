from flask import Flask, request, jsonify
import json
import pandas as pd
import os

app = Flask(__name__)

# Load the JSON data into memory (load once when the server starts)
with open('NSE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Convert JSON to Pandas DataFrame for efficient querying
df = pd.DataFrame(data)

@app.route('/get_instrument', methods=['GET'])
def get_instrument():
    """
    API Endpoint to fetch instrument key based on trading symbol.
    Query Parameters:
    - trading_symbol: Name of the stock (e.g., RELIANCE).
    - segment: Segment (default is NSE_EQ).
    - instrument_type: Instrument type (default is EQ).
    """
    # Get query parameters
    trading_symbol = request.args.get('trading_symbol')
    segment = request.args.get('segment', 'NSE_EQ')
    instrument_type = request.args.get('instrument_type', 'EQ')
    
    # Validate input
    if not trading_symbol:
        return jsonify({"error": "trading_symbol is required"}), 400
    
    # Filter data
    filtered_df = df[
        (df['segment'] == segment) &
        (df['instrument_type'] == instrument_type) &
        (df['trading_symbol'] == trading_symbol)
    ]
    
    # Check if any results are found
    if filtered_df.empty:
        return jsonify({"error": f"No instrument found for {trading_symbol}"}), 404
    
    # Convert to JSON-compatible response
    result = filtered_df.to_dict(orient='records')
    return jsonify(result)

# Run the Flask app
if __name__ == '__main__':
    # Bind to 0.0.0.0 and use the port provided by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
