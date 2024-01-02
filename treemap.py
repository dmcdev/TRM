
import pandas as pd
import matplotlib.pyplot as plt
import squarify  # you might need to install this package

import pandas as pd
import matplotlib.pyplot as plt
import squarify  # you might need to install this package

# Load your CSV data
# Replace 'your_data.csv' with the path to your CSV file
df = pd.read_csv('data.csv')

# Group data by category, then subcategory and product
grouped = df.groupby(['Category', 'Subcategory', 'Product']).size().reset_index(name='Counts')

# Get unique categories
categories = grouped['Category'].unique()

# Create a figure for the treemaps
fig, axes = plt.subplots(len(categories), 1, figsize=(12, 8 * len(categories)))

# Check if there's only one category, adjust axes to be a list
if len(categories) == 1:
    axes = [axes]

# Create a treemap for each category
for ax, category in zip(axes, categories):
    # Filter data for the category
    category_data = grouped[grouped['Category'] == category]
    
    # Prepare data for the treemap
    labels = category_data.apply(lambda x: f"{x['Subcategory']} > {x['Product']}", axis=1)
    sizes = category_data['Counts']
    
    # Create a treemap for the category
    squarify.plot(sizes=sizes, label=labels, alpha=0.6, ax=ax)
    ax.set_title(category)
    ax.axis('off')

plt.tight_layout()
plt.show()
