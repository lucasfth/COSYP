import glob
import re


lines = ["algorithm,bits,llc-load-misses,llc-store-misses"]
ctm_lines = []
co_lines = []
perf_files = sorted(
    glob.glob("perf-c*"), key=lambda x: int(x.split("-")[3].replace(".txt", ""))
)
for file in perf_files:
    content = open(file).read().replace(" ", "").replace("\n", "")
    matches = re.search(
        r"(\d+(?:,\d+)+)(?:LLC-load-misses)(\d+(?:,\d+)+)(?:LLC-store-misses)", content
    )
    if not matches:
        break

    load = matches[1].replace(",", "")
    store = matches[2].replace(",", "")

    _, algo, threads, bits = file.replace(".txt", "").split("-")
    algo = "count-then-move" if algo == "ctm" else "concurrent-output"
    line = ",".join([algo, bits, load, store])

    if algo == "count-then-move":
        ctm_lines.append(line)
    else:
        co_lines.append(line)

lines += ctm_lines
lines += co_lines

open("perf-metrics-bits.csv", "w").write("\n".join(lines))
