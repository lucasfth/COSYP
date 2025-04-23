import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# Set modern style
mpl.style.use('seaborn-v0_8')

# Load CSV file with performance metrics
perf_df = pd.read_csv("metrics-perf.csv")

# Create subplots - FLIPPED order as requested
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Define algorithms and get unique thread counts
algorithms = ['concurrent-output', 'count-then-move']
all_threads = sorted(perf_df['threads'].unique())

# Custom colors for algorithms
colors = ['#1f77b4', '#ff7f0e']  # Blue for concurrent-output, Orange for count-then-move
markers = ['o', 's']             # Circle for concurrent-output, Square for count-then-move

# Plot LLC Load Misses (now first subplot)
for i, algo in enumerate(algorithms):
    subset = perf_df[perf_df['algorithm'] == algo]
    ax1.plot(subset['threads'], 
             subset['llc-load-misses'],
             marker=markers[i],
             color=colors[i],
             label=algo)

ax1.set_title('(a) LLC Load Misses', fontsize=15)
ax1.set_xlabel('Threads', fontsize=15)
ax1.set_ylabel('LLC Load Misses', fontsize=15)
ax1.grid(True, linestyle='--', alpha=0.7)
ax1.set_xscale('log', base=2)  # Log scale for thread count
ax1.set_xticks(all_threads)
ax1.set_xticklabels(all_threads)
ax1.legend(loc='best')  # Add legend to each subplot

# Plot LLC Store Misses (now second subplot)
for i, algo in enumerate(algorithms):
    subset = perf_df[perf_df['algorithm'] == algo]
    ax2.plot(subset['threads'], 
             subset['llc-store-misses'],
             marker=markers[i],
             color=colors[i],
             label=algo)

ax2.set_title('(b) LLC Store Misses', fontsize=15)
ax2.set_xlabel('Threads', fontsize=15)
ax2.set_ylabel('LLC Store Misses', fontsize=15)
ax2.grid(True, linestyle='--', alpha=0.7)
ax2.set_xscale('log', base=2)  # Log scale for thread count
ax2.set_xticks(all_threads)
ax2.set_xticklabels(all_threads)
ax2.legend(loc='best')  # Add legend to each subplot

# Add formatted y-axis values (in millions)
def millions_formatter(x, pos):
    return f'{x/1e6:.1f}M'

ax1.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))
ax2.yaxis.set_major_formatter(plt.FuncFormatter(millions_formatter))

plt.tight_layout()
plt.savefig("cache_misses_comparison.png", bbox_inches='tight')
plt.show()
