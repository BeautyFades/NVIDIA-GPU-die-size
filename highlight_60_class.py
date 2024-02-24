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

# Plot points for the "60 class" with 100% opacity
scatter_60_class = sns.scatterplot(
    data=df[df['name'].str.contains('60')],
    x='generation_pretty_name',
    y='relative_core_count',
    hue='generation_name',
    palette=generation_colors,
    s=100,
    alpha=1.0,
    legend=False
)

# Plot points for the rest with transparency
scatter_others = sns.scatterplot(
    data=df[~df['name'].str.contains('60')],
    x='generation_pretty_name',
    y='relative_core_count',
    hue='generation_name',
    palette=generation_colors,
    s=100,
    alpha=0.18,
    legend=False
)

# Rotate x-axis labels for better readability
plt.xticks(rotation=0, ha='center')

# Set plot title and labels
plt.title('GPU Core Count Distribution by Generation', fontsize=16)
plt.xlabel('Generation Pretty Name', fontsize=14)
plt.ylabel('Relative Core Count (%)', fontsize=14)

# Add grid lines to make it easier to read
plt.grid(True, linestyle='--', alpha=0.7)


for i in range(len(df)):
    label = f"{df['name'][i]}: {df['relative_core_count'][i]:,.1f}%"
    alpha_value = 0.18 if '60' not in df['name'][i] else 1.0
    plt.annotate(label, (df['generation_pretty_name'][i], df['relative_core_count'][i]),
                 textcoords="offset points", xytext=(6, -3), ha='left', fontsize=11, fontweight='bold', color='black', alpha=alpha_value)
    plt.annotate(f"RP: {round(df['intra_gen_relative_perf'][i]*100, 2)}% | ${df['usd_msrp_price_at_launch'][i]}", (df['generation_pretty_name'][i], df['relative_core_count'][i]),
                 textcoords="offset points", xytext=(6, -11), ha='left', fontsize=9, fontweight='normal', color='black', alpha=alpha_value)

# Show the plot
plt.tight_layout()
plt.show()
