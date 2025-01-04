import requests
import pandas as pd

# Define the NREL AFDC API endpoint and API key
NREL_API_ENDPOINT = "https://developer.nrel.gov/api/alt-fuel-stations/v1.json"
NREL_API_KEY = "----" 

# Define parameters to filter for Washington State
nrel_params = {
    "api_key": NREL_API_KEY,
    "fuel_type": "ELEC",  # Electric stations only
    "state": "WA",  # Washington State
    "limit": 200,  # Adjust based on expected results
    "status": "E"  # Only operational stations
}

# Function to fetch NREL charging station data
def fetch_nrel_data():
    response = requests.get(NREL_API_ENDPOINT, params=nrel_params)
    if response.status_code == 200:
        print("NREL data fetched successfully!")
        return response.json().get("fuel_stations", [])
    else:
        print(f"Failed to fetch NREL data. Status code: {response.status_code}, Error: {response.text}")
        return None

# Process NREL data and append State
def process_nrel_data(data):
    processed_data = []
    for station in data:
        processed_data.append({
            "Station Name": station.get("station_name", "N/A"),
            "Street Address": station.get("street_address", "N/A"),
            "City": station.get("city", "N/A"),
            "State": "Washington",  # Add State
            "Access Days Time": station.get("access_days_time", "N/A"),
            "EV Level1 EVSE Num": station.get("ev_level1_evse_num", 0),
            "EV Level2 EVSE Num": station.get("ev_level2_evse_num", 0),
            "EV DC Fast Count": station.get("ev_dc_fast_num", 0),
            "EV Other Info": station.get("ev_pricing", "N/A"),
            "New Georeferenced Column": f"{station.get('latitude', 'N/A')}, {station.get('longitude', 'N/A')}"
        })
    return processed_data

# Save data to CSV
def save_to_csv(data, filename="nrel_charging_stations_washington.csv"):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")

# Main execution
if __name__ == "__main__":
    nrel_data = fetch_nrel_data()
    if nrel_data:
        processed_data = process_nrel_data(nrel_data)
        save_to_csv(processed_data)
