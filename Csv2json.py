import pandas as pd
import json

# Load CSV file
df = pd.read_csv('your_data.csv')

# Initialize an empty list to store the JSON data
json_data = []

# Add the root element
json_data.append({"name": "Root"})

# Process each row in the DataFrame
for index, row in df.iterrows():
    # For Category
    category_dict = {"name": row['Category'], "parent": "Root"}
    if category_dict not in json_data:
        json_data.append(category_dict)
    
    # For Subcategory
    subcategory_dict = {"name": row['Subcategory'], "parent": row['Category']}
    if subcategory_dict not in json_data:
        json_data.append(subcategory_dict)

    # For Product
    product_dict = {"name": row['Product'], "parent": row['Subcategory']}
    if product_dict not in json_data:
        json_data.append(product_dict)

# Save to JSON file
with open('output.json', 'w') as json_file:
    json.dump(json_data, json_file, indent=4)

print("JSON file created successfully.")
