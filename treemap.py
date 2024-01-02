#!/Users/zhenya/anaconda3/bin/python
import pandas as pd
import matplotlib.pyplot as plt
import squarify  # you might need to install this package

# Load your CSV data
# Replace 'your_data.csv' with the path to your CSV file
df = pd.read_csv('data.csv')

# Transform data into a hierarchical structure
hierarchy = df.groupby(['Category', 'Subcategory', 'Product']).size().reset_index(name='Counts')

# Prepare data for the treemap
labels = hierarchy.apply(lambda x: f"{x['Category']} > {x['Subcategory']} > {x['Product']}", axis=1)
sizes = hierarchy['Counts']

# Create a treemap
plt.figure(figsize=(12, 8))
squarify.plot(sizes=sizes, label=labels, alpha=0.6)
plt.axis('off')
plt.show()