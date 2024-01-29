import pandas as pd
import json

def create_flattened_hierarchy(csv_file):
    df = pd.read_csv(csv_file)
    result = []
    
    for _, row in df.iterrows():
        hierarchy = [row['Domain'], row['SubDomain'], row['Capability'], row['Component']]
        parent = ''
        for name in hierarchy:
            # Create an entry for each level in the hierarchy
            result.append({'id': name, 'parent': parent})
            parent = name
        
        # Add the ProdID with its additional attributes as an array
        prod_id_entry = {
            'id': row['ProdID'],
            'parent': parent,
            'attributes': [
                {'Heritage': row['Heritage']},
                {'Vendor': row['Vendor']},
                {'Intent': row['Intent']},
                {'Decom Date': str(row['Decom Date'])},  # Convert to string if necessary
                {'Cost': row['Cost']}
            ]
        }
        result.append(prod_id_entry)
    
    return result

# Path to your CSV file
csv_file_path = 'product.model.csv'

# Generate flattened hierarchy
flattened_hierarchy = create_flattened_hierarchy(csv_file_path)

# Convert to JSON
flattened_json = json.dumps(flattened_hierarchy, indent=4)

# Optionally, save to a file
with open('flattened_hierarchy.json', 'w') as outfile:
    outfile.write(flattened_json)

print("Flattened JSON file created successfully.")

