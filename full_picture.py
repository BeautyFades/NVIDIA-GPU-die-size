import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Read data from Excel file
file_path = 'tpu-data/gpu-db.xlsx'
sheet_name = 'OBT'
df = pd.read_excel(file_path, sheet_name=sheet_name)

# Set style
sns.set_style("whitegrid")

# Assign the same color to all generations
generation_palette = sns.color_palette("husl", n_colors=df['generation_name'].nunique())
generation_colors = dict(zip(df['generation_name'].unique(), generation_palette))

# Calculate relative core count
df['relative_core_count'] = (df['cuda_core_count'] / df.groupby('generation_name')['top_die_max_cuda_core_count'].transform('max')) * 100

# Create scatter plot
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=df,
    x='generation_pretty_name',
    y='relative_core_count',
    hue='generation_name',
    palette=generation_colors,
    s=100,
    legend=False
)

# Set y-axis limit to 100%
plt.ylim(0, 110)  # Adding extra space on the top

# Rotate x-axis labels for better readability
plt.xticks(rotation=0, ha='center')

# Set plot title and labels
plt.title('GPU Core Count Distribution by Generation', fontsize=16)
plt.xlabel('Generation Name', fontsize=14)
plt.ylabel('Relative Core Count (%)', fontsize=14)

# Add grid lines to make it easier to read
plt.grid(True, linestyle='--', alpha=0.7)

for i in range(len(df)):
    label = f"{df['name'][i]}: {df['relative_core_count'][i]:,.1f}%"
    plt.annotate(label, (df['generation_pretty_name'][i], df['relative_core_count'][i]),
                 textcoords="offset points", xytext=(6, -3), ha='left', fontsize=11, fontweight='bold', color='black')
    plt.annotate(f"RP: {round(df['intra_gen_relative_perf'][i]*100, 2)}% | ${df['usd_msrp_price_at_launch'][i]}", (df['generation_pretty_name'][i], df['relative_core_count'][i]),
                 textcoords="offset points", xytext=(6, -11), ha='left', fontsize=9, fontweight='normal', color='black')

# Show the plot
plt.tight_layout()
plt.show()