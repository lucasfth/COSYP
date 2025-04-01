import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Set modern style
mpl.style.use('seaborn-v0_8')

# Load CSV files
metrics_df = pd.read_csv("metrics.csv")

# Calculate throughput in millions of tuples per second
metrics_df['Throughput(MT/s)'] = metrics_df['data_size'] / \
    metrics_df['duration'] / 1000

# Split into two sets based on column "algorithm"
count_then_move_df = metrics_df[metrics_df['algorithm'] == 'count-then-move'].groupby(['algorithm', 'threads', 'hashbits'], as_index=False).mean()
concurrent_output_df = metrics_df[metrics_df['algorithm'] == 'concurrent-output'].groupby(['algorithm', 'threads', 'hashbits'], as_index=False).mean()

# Create subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), sharey=True)

# Get unique thread counts from data
all_threads = sorted(pd.concat([
    count_then_move_df['threads'],
    concurrent_output_df['threads'] if not concurrent_output_df.empty else pd.Series(
    )
]).unique())
num_threads = len(all_threads)

# Custom color palette for threads
colors = plt.cm.viridis_r(np.linspace(0, 1, num_threads))

# Plot Count-then-move results
for i, thread in enumerate(sorted(count_then_move_df['threads'].unique())):
    subset = count_then_move_df[count_then_move_df['threads'] == thread]
    ax1.plot(subset['hashbits'],
             subset['Throughput(MT/s)'],
             marker='o',
             color=colors[i],
             label=f'{thread} threads')

ax1.set_title('(a) Count-then-move', fontsize=15)
ax1.set_xlabel('Hash Bits', fontsize=15)
ax1.set_ylabel('Throughput (MT/s)', fontsize=15)
ax1.grid(True, linestyle='--', alpha=0.7)
max_hashbits = max(metrics_df['hashbits'])
ax1.set_xticks(range(1, max_hashbits + 1))

# Plot Concurrent-output results (if data exists)
if not concurrent_output_df.empty:
    for i, thread in enumerate(sorted(concurrent_output_df['threads'].unique())):
        subset = concurrent_output_df[concurrent_output_df['threads'] == thread]
        ax2.plot(subset['hashbits'],
                 subset['Throughput(MT/s)'],
                 marker='s',
                 color=colors[i],
                 label=f'{thread} threads')

ax2.set_title('(b) Concurrent-output', fontsize=15)
ax2.set_xlabel('Hash Bits', fontsize=15)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.set_xticks(range(1, max_hashbits + 1))

# Common legend
handles, labels = ax1.get_legend_handles_labels()
fig.legend(handles, labels, loc='upper center',
           ncol=min(7, len(handles)), bbox_to_anchor=(0.5, 1.05))

# Add extra information
plt.figtext(0.5, -0.05, f"System: {metrics_df['cores'].iloc[0]} cores, {metrics_df['memory'].iloc[0]/1e9:.1f} GB memory",
            ha='center', fontsize=10, bbox={'facecolor': 'lightgray', 'alpha': 0.5, 'pad': 5})

plt.tight_layout()
plt.savefig("throughput_comparison.png", bbox_inches='tight')
plt.show()
