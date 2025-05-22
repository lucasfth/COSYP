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
IDLE_POWER = 1.8 # W

NUM_RUNS = 10

# ===== FIND EMOJI =====


def find_emoji(lang):
    emojis = {
        "c": "🐀",
        "java": "☕",
        "javascript": "🚧",
        "typescript": "🛄",
        "zig": "🦎",
        "ruby": "💎",
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
        energy += (power-IDLE_POWER) * interval
        time.sleep(interval)

    if process.returncode == 0:
        duration = time.time() - start
        print(f"\t✅ Finished in {duration:.2f}s, Energy: {energy:.2f} J")
        return (energy, duration)

    print(f"\t❌  Failed with exit code: {process.returncode}")
    return (0.0, 0.0)


# ===== BENCHMARK DISCOVERY =====


def find_benchmark_dirs():
    benchmarks = {}
    for lang in ["c","java", "javascript", "typescript", "zig", "ruby"]:
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
            if lang in ["typescript", "javascript", "ruby"]:
                continue
            try:
                print(f"{find_emoji(lang)} Building {lang}-{name}")
                build_energy, build_duration = measure_energy(["make", "build"], cwd=path)

                results.append(
                    {
                        "lang": lang,
                        "algorithm": name,
                        "energy": round(build_energy, 4),
                        "type": "build",
                        "duration": round(build_duration, 4)
                    })
            except Exception as e:
                print(f"\t❌ Failed for {lang}-{name}: {e}")
                results.append(
                    {
                        "lang": lang,
                        "algorithm": name,
                        "energy": "failed",
                        "type": "build",
                        "duration": 0.0
                    }
                )

# ===== RUN =====
# And run each benchmark NUM_RUNS times


def run(benchmarks, results):
    print("\n\n🏃 Running -----------\n")

    for name, impls in benchmarks.items():
        print(f"Running {name}")

        for lang, path in impls.items():
            total_run_energy = 0.0
            total_run_duration = 0.0
            successful_runs = 0
            for _ in range(NUM_RUNS):
                print(f"{find_emoji(lang)} Running {lang}-{name}")
                run_energy, run_duration = measure_energy(["make", "run"], cwd=path)
                if run_energy > 0:
                    total_run_energy += run_energy
                    successful_runs += 1
                    total_run_duration += run_duration
            results.append(
                {
                    "lang": lang,
                    "algorithm": name,
                    "energy": round(total_run_energy / successful_runs, 4)
                    if successful_runs == NUM_RUNS
                    else "failed",
                    "type": "run",
                    "duration": round(total_run_duration / successful_runs, 4)
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
                "energy",
                "type",
                "duration"
            ],
        )
        writer.writeheader()
        writer.writerows(results)

    print(f"\n📄 Results written to: {CSV_OUTPUT_FILE}")

if __name__ == "__main__":
    main()
