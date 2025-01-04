import requests
import pandas as pd

# WSDOT Access Code
access_code = "----"

# WSDOT API endpoint for GetTrafficFlowsAsJson
url = f"http://wsdot.wa.gov/Traffic/api/TrafficFlow/TrafficFlowREST.svc/GetTrafficFlowsAsJson?AccessCode={access_code}"

def fetch_all_traffic_flows():
    """
    Fetch all available traffic flow data from WSDOT API.
    """
    try:
        print(f"Fetching traffic flow data from: {url}")
        response = requests.get(url)

        if response.status_code == 200:
            print("Traffic flow data fetched successfully!")
            return response.json()  # Assuming the API returns JSON data
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"Error while fetching traffic flow data: {e}")
        return None

def process_traffic_flows(data):
    """
    Process the traffic flow data into a DataFrame.
    """
    try:
        if data:
            df = pd.DataFrame(data)  # Assuming data is a list of dictionaries
            print(f"Data successfully processed into a DataFrame with {len(df)} records.")
            return df
        else:
            print("No data to process.")
            return None
    except Exception as e:
        print(f"Error while processing traffic flow data: {e}")
        return None

if __name__ == "__main__":
    traffic_flows = fetch_all_traffic_flows()
    if traffic_flows:
        df = process_traffic_flows(traffic_flows)
        if df is not None:
            # Save to CSV for further analysis
            df.to_csv("AllTrafficFlows.csv", index=False)
            print("Traffic flow data saved as 'AllTrafficFlows.csv'")
