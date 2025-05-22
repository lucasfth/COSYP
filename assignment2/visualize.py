import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# --- Configuration ---
CSV_FILE = "energy_results.csv"
OUTPUT_DIR = "."  # Directory to save plots
BUILD_PLOT_FILE = f"{OUTPUT_DIR}/build_energy_comparison.png"
RUN_PLOT_FILE = f"{OUTPUT_DIR}/run_energy_comparison.png"
TOTAL_PLOT_FILE = f"{OUTPUT_DIR}/total_energy_comparison.png"
RELATIVE_RUN_PLOT_FILE = f"{OUTPUT_DIR}/relative_run_energy.png"

# Define a consistent color palette for languages
LANGUAGE_COLORS = {
    'c': '#1f77b4',       # blue
    'java': '#ff7f0e',    # orange
    'javascript': '#2ca02c',  # green
    'typescript': '#d62728',  # red
    'zig': '#9467bd',     # purple
    'ruby': '#8c564b'     # brown
    # Add more languages and colors as needed
}

# --- Data Loading and Preprocessing ---


def load_and_preprocess_data(csv_file):
    df = pd.read_csv(csv_file)

    # Convert 'energy' column to numeric, coercing 'failed' to NaN
    df['energy'] = pd.to_numeric(df['energy'], errors='coerce')

    # Drop rows where energy is NaN (i.e., 'failed' runs)
    df_cleaned = df.dropna(subset=['energy']).copy()

    # Combine lang and algorithm for easier labeling
    df_cleaned['label'] = df_cleaned['lang'] + '_' + df_cleaned['algorithm']
    return df_cleaned

# --- Plotting Functions ---


def create_bar_chart(df, energy_type, title, filename):
    """
    Creates a grouped bar chart for energy consumption with logarithmic y-axis.
    """
    # Filter for the specific energy type (build/run)
    df_filtered = df[df['type'] == energy_type]

    # Create pivot table for easy plotting
    pivot_df = df_filtered.pivot_table(
        index='algorithm', columns='lang', values='energy')

    # Sort columns (languages) alphabetically for consistent ordering
    pivot_df = pivot_df.sort_index(axis=1)

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))

    # Extract colors for the languages present in this dataset
    colors = [LANGUAGE_COLORS.get(lang, f'C{i}')
              for i, lang in enumerate(pivot_df.columns)]

    # Plot with consistent colors
    pivot_df.plot(kind='bar', ax=ax, width=0.8, color=colors)

    # Set logarithmic scale for y-axis
    ax.set_yscale('log')

    ax.set_title(title, fontsize=16)
    ax.set_xlabel('Benchmark Algorithm', fontsize=12)
    ax.set_ylabel(
        f'Energy ({energy_type.capitalize()} - Joules) [log scale]', fontsize=12)
    ax.tick_params(axis='x', rotation=45)

    # Format y-axis for log scale - no scientific notation needed with log scale
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

    ax.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"📊 Saved '{energy_type}' plot to {filename}")
    plt.close(fig)  # Close the figure to free memory


def create_relative_run_chart(df, filename):
    """
    Creates a bar chart showing run energy relative to C with logarithmic y-axis.
    """
    df_run = df[df['type'] == 'run'].copy()

    # Calculate C baseline
    df_c_baseline = df_run[df_run['lang'] == 'c'].set_index('algorithm')[
        'energy']

    # Calculate relative energy for other languages
    df_relative = df_run.set_index(['algorithm', 'lang'])['energy'].unstack()

    # Divide by C baseline, handle cases where C might be 0 or NaN
    for col in df_relative.columns:
        if col != 'c' and col in df_relative.columns:
            df_relative[col] = df_relative[col] / df_c_baseline
        elif col == 'c':
            df_relative[col] = 1.0  # C is relative to itself

    # Remove 'c' column if we only want comparisons
    df_relative = df_relative.drop(columns='c', errors='ignore')

    # Sort for consistent plotting
    df_relative = df_relative.sort_index(axis=0)
    df_relative = df_relative.sort_index(
        axis=1)  # Sort languages alphabetically

    # Plotting
    fig, ax = plt.subplots(figsize=(14, 8))

    # Extract colors for the languages present in this dataset
    colors = [LANGUAGE_COLORS.get(lang, f'C{i}')
              for i, lang in enumerate(df_relative.columns)]

    # Plot with consistent colors
    df_relative.plot(kind='bar', ax=ax, width=0.8, color=colors)

    # Set logarithmic scale for y-axis
    ax.set_yscale('log')

    ax.set_title(
        'Run Energy Consumption Relative to C Language [log scale]', fontsize=16)
    ax.set_xlabel('Benchmark Algorithm', fontsize=12)
    ax.set_ylabel('Relative Energy (C = 1.0) [log scale]', fontsize=12)
    ax.tick_params(axis='x', rotation=45)
    ax.axhline(1.0, color='red', linestyle='--',
               linewidth=0.8, label='C Baseline (1.0)')
    ax.legend(title='Language', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(filename)
    print(f"📊 Saved relative run energy plot to {filename}")
    plt.close(fig)

# --- Main Execution ---


def main():
    df_cleaned = load_and_preprocess_data(CSV_FILE)

    # 1. Plot Build Energy
    create_bar_chart(df_cleaned, 'build',
                     'Build Energy Consumption Across Languages', BUILD_PLOT_FILE)

    # 2. Plot Run Energy
    create_bar_chart(df_cleaned, 'run',
                     'Run Energy Consumption Across Languages', RUN_PLOT_FILE)

    # 3. Calculate and Plot Total Energy
    df_total = df_cleaned.groupby(['lang', 'algorithm'])[
        'energy'].sum().reset_index()
    # Add a 'type' column for re-using the plotting function
    df_total['type'] = 'total'
    create_bar_chart(df_total, 'total',
                     'Total Energy Consumption (Build + Run)', TOTAL_PLOT_FILE)

    # 4. Plot Relative Run Energy (to C)
    create_relative_run_chart(df_cleaned, RELATIVE_RUN_PLOT_FILE)


if __name__ == "__main__":
    main()
