import pandas as pd
import googlemaps
from datetime import datetime
import time

# Load the data
file_path = "AllTrafficFlows.csv"  # Replace with your file path
data = pd.read_csv(file_path)

# Initialize Google Maps client
API_KEY = "----"  
gmaps = googlemaps.Client(key=API_KEY)

# Function to classify congestion levels
def classify_congestion(flow_value):
    if flow_value <= 2:
        return "Severe Congestion"
    elif 3 <= flow_value <= 5:
        return "Moderate Congestion"
    else:
        return "Free Flow"

# Function to convert /Date() format to readable timestamp
def convert_date(ms_date):
    try:
        timestamp = int(ms_date.split('(')[1].split('-')[0]) / 1000
        return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return None

# Reverse geocoding to find street names using Google Maps API
geocode_cache = {}

def get_street_name(lat, lon):
    coord_key = (lat, lon)
    if coord_key in geocode_cache:
        return geocode_cache[coord_key]
    
    try:
        results = gmaps.reverse_geocode((lat, lon))
        if results:
            street_name = results[0]['formatted_address']
            geocode_cache[coord_key] = street_name
            return street_name
        else:
            return "Unknown"
    except Exception as e:
        print(f"Error fetching street name for ({lat}, {lon}): {e}")
        return "Unknown"

# Process the dataset
processed_data = []
for index, row in data.iterrows():
    location = eval(row["FlowStationLocation"])  # Parse the location field
    description = location["Description"]
    latitude = location["Latitude"]
    longitude = location["Longitude"]

    # If the description is "Unknown," perform reverse geocoding
    if description == "Unknown":
        description = get_street_name(latitude, longitude)
        time.sleep(0.1)  # Avoid hitting rate limits

    # Process the row
    processed_data.append({
        "Street": description,
        "Direction": location["Direction"],
        "Latitude": latitude,
        "Longitude": longitude,
        "Congestion_Level": classify_congestion(row["FlowReadingValue"]),
        "Timestamp": convert_date(row["Time"]),
    })

# Create a new DataFrame
processed_df = pd.DataFrame(processed_data)

# Save the processed data to a new CSV
output_file = "ProcessedTrafficFlows.csv"
processed_df.to_csv(output_file, index=False)
print(f"Processed data saved to {output_file}")

# Display a preview of the processed data
print(processed_df.head())
