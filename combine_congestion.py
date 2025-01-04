import pandas as pd

# Load the datasets
all_traffic_flows_path = "AllTrafficFlows.csv"  # Path to AllTrafficFlows.csv
processed_traffic_flows_path = "ProcessedTrafficFlows.csv"  # Path to ProcessedTrafficFlows.csv

all_traffic_flows = pd.read_csv(all_traffic_flows_path)
processed_traffic_flows = pd.read_csv(processed_traffic_flows_path)

# Rename FlowReadingValue to Congestion_Level
all_traffic_flows.rename(columns={"FlowReadingValue": "Congestion_Level"}, inplace=True)

# Select required columns
all_traffic_flows_selected = all_traffic_flows[["FlowDataID", "Congestion_Level", "Region", "StationName"]]
processed_traffic_flows_selected = processed_traffic_flows[["Street", "Direction", "Latitude", "Longitude", "Timestamp"]]

# Merge the datasets
merged_data = pd.concat([all_traffic_flows_selected, processed_traffic_flows_selected], axis=1)

# Save the merged dataset to TrafficFlows.csv
output_file = "TrafficFlows.csv"
merged_data.to_csv(output_file, index=False)

print(f"Traffic flows data saved to {output_file}")
