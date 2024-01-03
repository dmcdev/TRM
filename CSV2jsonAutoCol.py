import pandas as pd
import json

# Load CSV file
df = pd.read_csv('your_data.csv')

# Get column names
columns = df.columns.tolist()

# Initialize an empty list to store the JSON data
json_data = []

# Function to add items to JSON data if not already present
def add_to_json(name, parent):
    item_dict = {"name": name, "parent": parent}
    if item_dict not in json_data:
        json_data.append(item_dict)

# Process each row in the DataFrame
for index, row in df.iterrows():
    # Add elements based on column hierarchy
    for i in range(1, len(columns)):
        add_to_json(row[columns[i]], row[columns[i-1]] if i > 0 else None)

# Save to JSON file
with open('output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created successfully.")
