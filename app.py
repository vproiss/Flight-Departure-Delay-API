from flask import Flask, request, jsonify, render_template
from fetch_data import fetch_data
from apscheduler.schedulers.background import BackgroundScheduler
import pandas as pd

app = Flask(__name__)

# Fetch the data and load it into a pandas DataFrame.
data = pd.DataFrame(fetch_data())

def update_data():
    """
    This function gets the data and updates the global DataFrame if new data is available.
    """
    global data
    new_data = fetch_data()
    if new_data:
        data = pd.DataFrame(new_data)
        print(f"Data updated: {len(data)} rows")

# Set up a scheduler to update the data every 30 minutes.
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_data, trigger="interval", minutes=30)
scheduler.start()

@app.route("/")
def home():
    """
    Render the home page.
    """
    return render_template("index.html")

@app.route("/api/flights", methods=["GET"])
def get_flights():
    """
    API endpoint to get the flight information with filtering by destination and airline.
    
    Query Parameters:
    - destination (str): Code of the destination airport.
    - airline (str): Code of the airline.

    Returns:
    - JSON: A list of flights matching the filter.
    """
    destination = request.args.get('destination')
    airline = request.args.get('airline')
    
    filtered_data = data
    
    if destination:
        filtered_data = filtered_data[filtered_data['destination'] == destination]
    if airline:
        filtered_data = filtered_data[filtered_data['airline'] == airline]
    
    filtered_data = filtered_data.drop_duplicates(subset=['flight_number', 'airline'])
    
    return jsonify(filtered_data.to_dict(orient='records'))

@app.route("/api/destinations", methods=["GET"])
def get_destinations():
    """
    API endpoint to get the list of unique destinations.

    Returns:
    - JSON: A list of unique destination codes.
    """
    if data.empty:
        return jsonify([])
    destinations = data['destination'].unique().tolist()
    return jsonify(destinations)

@app.route("/api/airlines", methods=["GET"])
def get_airlines():
    """
    API endpoint to get the list of unique airlines.

    Returns:
    - JSON: A list of unique airline codes.
    """
    if data.empty:
        return jsonify([])
    airlines = data['airline'].unique().tolist()
    return jsonify(airlines)

if __name__ == "__main__":
    print(f"Initial data fetched: {len(data)} rows")
    app.run(debug=True)




























