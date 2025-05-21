import os
import subprocess
import time
import glob
import requests
import csv
import matplotlib.pyplot as plt

PROMETHEUS_URL = "http://localhost:9090"
PROMQL = "sum(pi5_volt * ignoring(id) pi5_current)"
ROOT_DIR = "."
CSV_OUTPUT_FILE = "energy_results.csv"

NUM_RUNS = 2

# ===== FIND EMOJI =====


def find_emoji(lang):
    emojis = {
        "c": "🐀",
        "java": "☕",
        "javascript": "🚧",
        "typescript": "🛄",
        "zig": "🦎",
    }
    return emojis.get(lang, "❓")

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


def measure_energy(cmd, cwd):
    interval = 0.1  # seconds
    energy = 0.0
    print(f"\t▶️  Measuring: {' '.join(cmd)} (cwd={cwd})")
    start = time.time()
    process = subprocess.Popen(
        cmd, cwd=cwd, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT
    )

    while process.poll() is None:
        power = read_power()
        energy += power * interval
        time.sleep(interval)

    if process.returncode == 0:
        duration = time.time() - start
        print(f"\t✅ Finished in {duration:.2f}s, Energy: {energy:.2f} J")
        return energy

    print(f"\t❌  Failed with exit code: {process.returncode}")
    return 0.0


# ===== BENCHMARK DISCOVERY =====


def find_benchmark_dirs():
    benchmarks = {}
    for lang in ["c", "java", "javascript", "typescript", "zig"]:
        lang_dir = os.path.join(ROOT_DIR, lang)
        if not os.path.isdir(lang_dir):
            continue
        for bench_dir in glob.glob(os.path.join(lang_dir, "*")):
            if os.path.isdir(bench_dir):
                name = os.path.basename(bench_dir).lower()
                benchmarks.setdefault(name, {})[lang] = bench_dir
    return benchmarks

# ===== BUILD =====


def build(benchmarks, results):
    print("🏗️ Building -----------\n")

    for name, impls in benchmarks.items():
        for lang, path in impls.items():
            try:
                print(f"{find_emoji(lang)} Building {lang}-{name}")
                build_energy = measure_energy(["make", "build"], cwd=path)

                results.append(
                    {
                        "lang": lang,
                        "algorithm": name,
                        "build_energy": round(build_energy, 4),
                    })
            except Exception as e:
                print(f"\t❌ Failed for {lang}-{name}: {e}")
                results.append(
                    {
                        "lang": lang,
                        "algorithm": name,
                        "build_energy": "failed",
                    }
                )

# ===== RUN =====
# And run each benchmark NUM_RUNS times


def run(benchmarks, results):
    print("\n\n🏃 Running -----------\n")

    for name, impls in benchmarks.items():
        for lang, path in impls.items():
            total_run_energy = 0.0
            successful_runs = 0
            for _ in range(NUM_RUNS):
                print(f"{find_emoji(lang)} Running {lang}-{name}")
                run_energy = measure_energy(["make", "run"], cwd=path)
                if run_energy > 0:
                    total_run_energy += run_energy
                    successful_runs += 1
            results.append(
                {
                    "lang": lang,
                    "algorithm": name,
                    "run_energy": round(total_run_energy / successful_runs, 4)
                    if successful_runs == NUM_RUNS
                    else "failed",
                }
            )


# ===== MAIN =====
def main():
    benchmarks = find_benchmark_dirs()
    results = []

    build(benchmarks, results)

    run(benchmarks, results)

    # Write CSV
    with open(CSV_OUTPUT_FILE, mode="w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "lang",
                "algorithm",
                "build_energy",
                "run_energy",
                "total_energy",
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\n📄 Results written to: {CSV_OUTPUT_FILE}")
    plot_results(results)


# ===== VISUALIZATION =====


def plot_results(results, output_file="energy_results.png"):
    filtered = [r for r in results if r["total_energy"] != "failed"]

    if not filtered:
        print("⚠️  No successful results to plot.")
        return

    labels = [f"{r['lang']}-{r['algorithm']}" for r in filtered]
    build_energy = [r["build_energy"] for r in filtered]
    run_energy = [r["run_energy"] for r in filtered]

    x = range(len(labels))
    plt.figure(figsize=(12, 6))
    plt.barh(x, build_energy, label="Build Energy", color="orange")
    plt.barh(x, run_energy, left=build_energy,
             label="Run Energy", color="skyblue")

    plt.yticks(x, labels)
    plt.xlabel("Energy (Joules)")
    plt.title("Build vs Run Energy Consumption")
    plt.legend()
    plt.tight_layout()
    plt.savefig(output_file)
    print(f"📊 Chart saved to: {output_file}")


if __name__ == "__main__":
    main()
