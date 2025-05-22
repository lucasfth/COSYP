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
    'c': '#BF71FF',       # blue
    'java': '#4F3C30',    # c0ffee
    'javascript': '#F7E018',  # yellow
    'typescript': '#2E79C7',  # blue
    'zig': '#F7A41E',     # yellowish
    'ruby': '#D91405'     # red
    # Add more languages and colors as needed
}

# --- Data Loading and Preprocessing ---


def load_and_preprocess_data(csv_file):
    df = pd.read_csv(csv_file)

    # Convert 'energy' column to numeric, coercing 'failed' to NaN
    df['energy'] = pd.to_numeric(df['energy'], errors='coerce')
    df['power'] = pd.to_numeric(
        df['energy'], errors='coerce') / pd.to_numeric(df['duration'], errors='coerce')

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


def generate_latex_tables(df, output_file):
    """
    Generates LaTeX tables showing energy usage by language and algorithm.
    """
    # Make sure we're working with numeric data
    df = df.copy()
    df['energy'] = pd.to_numeric(df['energy'], errors='coerce')

    # Group by language and type, then sum across algorithms
    lang_summary = df.groupby(['lang', 'type'])['energy'].sum().reset_index()
    lang_summary_pivot = lang_summary.pivot(
        index='lang', columns='type', values='energy')

    # Add a total column
    if 'build' in lang_summary_pivot.columns and 'run' in lang_summary_pivot.columns:
        lang_summary_pivot['total'] = lang_summary_pivot['build'].fillna(
            0) + lang_summary_pivot['run'].fillna(0)

    # Round values for readability
    lang_summary_pivot = lang_summary_pivot.round(2)

    # Create LaTeX table by language - with better formatting
    lang_table = lang_summary_pivot.to_latex(
        float_format="%.2f",
        na_rep="-",
        index_names=False,  # Don't show "lang" as index name
        caption="Energy Usage by Language (Joules)",
        label="tab:energy_by_language"
    )

    # Group by algorithm and type, then sum across languages
    algo_summary = df.groupby(['algorithm', 'type'])[
        'energy'].sum().reset_index()
    algo_summary_pivot = algo_summary.pivot(
        index='algorithm', columns='type', values='energy')

    # Add a total column
    if 'build' in algo_summary_pivot.columns and 'run' in algo_summary_pivot.columns:
        algo_summary_pivot['total'] = algo_summary_pivot['build'].fillna(
            0) + algo_summary_pivot['run'].fillna(0)

    # Round values for readability
    algo_summary_pivot = algo_summary_pivot.round(2)

    # Create LaTeX table by algorithm - with better formatting
    algo_table = algo_summary_pivot.to_latex(
        float_format="%.2f",
        na_rep="-",
        index_names=False,  # Don't show "algorithm" as index name
        caption="Energy Usage by Algorithm (Joules)",
        label="tab:energy_by_algorithm"
    )

    # Create detailed table with each language-algorithm combination
    detailed = df.pivot_table(
        index=['lang', 'algorithm'],
        columns='type',
        values='energy',
        aggfunc='sum'
    )

    # Add a total column
    if 'build' in detailed.columns and 'run' in detailed.columns:
        detailed['total'] = detailed['build'].fillna(
            0) + detailed['run'].fillna(0)

    # Round values
    detailed = detailed.round(2)

    # Create LaTeX table for detailed view - with better formatting
    detailed_table = detailed.to_latex(
        float_format="%.2f",
        na_rep="-",
        multirow=True,  # Use multirow for the hierarchical index
        caption="Detailed Energy Usage by Language and Algorithm (Joules)",
        label="tab:detailed_energy"
    )

    # Write all tables to the output file
    with open(output_file, 'w') as f:
        f.write("% Energy Usage Tables for LaTeX\n\n")

        # Language summary table
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Energy Usage by Language (Joules)}\n")
        f.write("\\label{tab:energy_by_language}\n")
        f.write("\\begin{tabular}{lrrr}\n")
        f.write("\\toprule\n")
        f.write("Language & Build & Run & Total \\\\\n")
        f.write("\\midrule\n")

        # Add rows manually for better control
        for lang in sorted(lang_summary_pivot.index):
            row = lang_summary_pivot.loc[lang]
            build_val = f"{row.get('build', 0):.2f}" if 'build' in row and not pd.isna(
                row['build']) else "-"
            run_val = f"{row.get('run', 0):.2f}" if 'run' in row and not pd.isna(
                row['run']) else "-"
            total_val = f"{row.get('total', 0):.2f}" if 'total' in row and not pd.isna(
                row['total']) else "-"

            f.write(f"{lang} & {build_val} & {run_val} & {total_val} \\\\\n")

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n\n")

        # Algorithm summary table
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write("\\caption{Energy Usage by Algorithm (Joules)}\n")
        f.write("\\label{tab:energy_by_algorithm}\n")
        f.write("\\begin{tabular}{lrrr}\n")
        f.write("\\toprule\n")
        f.write("Algorithm & Build & Run & Total \\\\\n")
        f.write("\\midrule\n")

        # Add rows manually for better control
        for algo in sorted(algo_summary_pivot.index):
            row = algo_summary_pivot.loc[algo]
            build_val = f"{row.get('build', 0):.2f}" if 'build' in row and not pd.isna(
                row['build']) else "-"
            run_val = f"{row.get('run', 0):.2f}" if 'run' in row and not pd.isna(
                row['run']) else "-"
            total_val = f"{row.get('total', 0):.2f}" if 'total' in row and not pd.isna(
                row['total']) else "-"

            f.write(f"{algo} & {build_val} & {run_val} & {total_val} \\\\\n")

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n\n")

        # For the detailed table, let's also create a manual version
        f.write("\\begin{table}[htbp]\n")
        f.write("\\centering\n")
        f.write(
            "\\caption{Detailed Energy Usage by Language and Algorithm (Joules)}\n")
        f.write("\\label{tab:detailed_energy}\n")
        f.write("\\begin{tabular}{llrrr}\n")
        f.write("\\toprule\n")
        f.write("Language & Algorithm & Build & Run & Total \\\\\n")
        f.write("\\midrule\n")

        # Group by language to create a more organized table
        for lang in sorted(detailed.index.get_level_values('lang').unique()):
            lang_rows = detailed.xs(lang, level='lang')
            first_row = True

            for algo in sorted(lang_rows.index):
                row = lang_rows.loc[algo]
                build_val = f"{row.get('build', 0):.2f}" if 'build' in row and not pd.isna(
                    row['build']) else "-"
                run_val = f"{row.get('run', 0):.2f}" if 'run' in row and not pd.isna(
                    row['run']) else "-"
                total_val = f"{row.get('total', 0):.2f}" if 'total' in row and not pd.isna(
                    row['total']) else "-"

                if first_row:
                    f.write(
                        f"{lang} & {algo} & {build_val} & {run_val} & {total_val} \\\\\n")
                    first_row = False
                else:
                    f.write(
                        f" & {algo} & {build_val} & {run_val} & {total_val} \\\\\n")

            # Add a midrule between languages
            if lang != sorted(detailed.index.get_level_values('lang').unique())[-1]:
                f.write("\\midrule\n")

        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")

    print(f"📄 LaTeX tables saved to {output_file}")

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

    # 5. Generate LaTeX Tables
    LATEX_OUTPUT_FILE = f"{OUTPUT_DIR}/energy_usage_tables.tex"
    generate_latex_tables(df_cleaned, LATEX_OUTPUT_FILE)


if __name__ == "__main__":
    main()
