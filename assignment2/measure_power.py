import matplotlib.pyplot as plt
import os
import subprocess
import time
import glob
import requests
import csv


PROMETHEUS_URL = "http://localhost:9090"
PROMQL = "sum(pi5_volt * ignoring(id) pi5_current)"
ROOT_DIR = "."  # Root directory of the language folders
CSV_OUTPUT_FILE = "energy_results.csv"

# ===== POWER MEASUREMENT VIA PROMETHEUS =====


def read_power():
    try:
        response = requests.get(
            f"{PROMETHEUS_URL}/api/v1/query", params={"query": PROMQL}, timeout=2
        )
        response.raise_for_status()
        data = response.json()
        result = data.get("data", {}).get("result", [])
        if result and "value" in result[0]:
            _, value = result[0]["value"]
            return float(value)
        else:
            print("⚠️  No power data available.")
            return 0.0
    except Exception as e:
        print(f"⚠️  Error querying Prometheus: {e}")
        return 0.0


# ===== ENERGY MEASUREMENT =====


def run_and_measure(cmd, cwd):
    interval = 0.5  # seconds
    energy = 0.0

    print(f"▶️  Running: {' '.join(cmd)} (cwd={cwd})")
    start = time.time()
    # process = subprocess.Popen(cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    for i in range(0, 300):
        power = read_power()
        energy += power * interval
        time.sleep(interval)

    duration = time.time() - start
    print(f"✅ Finished in {duration:.2f}s, Energy: {energy:.2f} J")
    return energy


# ===== COMPILATION LOGIC =====


def compile_c(file_path):
    exe = os.path.splitext(file_path)[0]
    subprocess.run(["gcc", "-O3", file_path, "-o", exe, "-lm"], check=True)
    return f"./{os.path.basename(exe)}"


def compile_rust(file_path):
    exe = os.path.splitext(file_path)[0]
    subprocess.run(["rustc", "-C", "opt-level=3", file_path, "-o", exe], check=True)
    return f"./{os.path.basename(exe)}"


def compile_java(file_path):
    subprocess.run(["javac", file_path], check=True)
    class_name = os.path.splitext(os.path.basename(file_path))[0]
    return ["java", class_name]


# ===== COMMAND GENERATION =====


def get_command(lang, file_path):
    filename = os.path.basename(file_path)
    cwd = os.path.dirname(file_path)

    if lang == "c":
        exe = compile_c(file_path)
        return [exe, "500000"], cwd
    elif lang == "rust":
        exe = compile_rust(file_path)
        return [exe], cwd
    elif lang == "java":
        return compile_java(file_path), cwd
    elif lang == "python":
        return ["python3", "-OO", filename, "500000"], cwd
    elif lang == "ruby":
        return ["ruby", "--yjit", "-W0", filename, "500000"], cwd
    else:
        raise ValueError(f"Unsupported language: {lang}")


# ===== BENCHMARK DISCOVERY =====


def find_benchmark_files():
    benchmarks = {}
    extensions = {
        "c": ".c",
        # 'java': '.java',
        # 'rust': '.rs',
        "python": ".py",
        "ruby": ".rb",
    }

    for lang, ext in extensions.items():
        lang_dir = os.path.join(ROOT_DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        files = glob.glob(os.path.join(lang_dir, f"*{ext}"))
        for file_path in files:
            name = os.path.splitext(os.path.basename(file_path))[0].lower()
            benchmarks.setdefault(name, {})[lang] = file_path
    return benchmarks


def plot_results(results, output_file="energy_results.png"):
    filtered = [r for r in results if r["energy"] != "failed"]

    if not filtered:
        print("⚠️  No successful results to plot.")
        return

    labels = [f"{r['lang']}-{r['algorithm']}" for r in filtered]
    energies = [float(r["energy"].replace("J", "")) for r in filtered]

    plt.figure(figsize=(10, 6))
    bars = plt.barh(labels, energies, color="skyblue")
    plt.xlabel("Energy (Joules)")
    plt.title("Energy Consumption by Implementation")
    plt.grid(axis="x", linestyle="--", alpha=0.7)

    for bar, energy in zip(bars, energies):
        plt.text(
            bar.get_width(),
            bar.get_y() + bar.get_height() / 2,
            f"{energy:.2f} J",
            va="center",
        )

    plt.tight_layout()
    plt.savefig(output_file)
    print(f"📊 Chart saved to: {output_file}")


# ===== MAIN SCRIPT =====


def main():
    benchmarks = find_benchmark_files()
    results = []

    for name, impls in benchmarks.items():
        if name != "nbody":
            continue
        print(f"\n🚀 Benchmark: {name}")
        for lang, path in impls.items():
            try:
                cmd, cwd = get_command(lang, path)
                energy = run_and_measure(cmd, cwd)
                results.append(
                    {"lang": lang, "algorithm": name, "energy": f"{round(energy, 4)}J"}
                )
            except Exception as e:
                print(f"❌ Failed for {lang}-{name}: {e}")
                results.append({"lang": lang, "algorithm": name, "energy": "failed"})

    # Write results to CSV
    with open(CSV_OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["lang", "algorithm", "energy"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

    print(f"\n📄 Results written to: {CSV_OUTPUT_FILE}")

    # Plot the results
    plot_results(results)


if __name__ == "__main__":
    main()
