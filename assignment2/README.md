# Measure Power

This repository was created during the course `Computer Systems Performance` at the IT University of Copenhagen - by [Andreas Trøstrup](https://github.com/duckth), [Frederik Petersen](https://github.com/fredpetersen), and [Lucas Hanson](https://github.com/lucasfth).

It was created to compare the energy consumption of different programming languages, specifically C, Java, JavaScript, TypeScript, Ruby, and Zig.

The paper concluded that even though there is a tendency for compiled languages to use less energy it is hard to draw strict conclusions from the data.
This is due to that implmentation, the transpiler chosen, the libraries used, and the hardware used all have a significant impact on the energy consumption of the program.

This program was run on a Raspberry Pi 5 with 8GB of RAM.

<details><summary><h2>Language dependencies</h2></summary>
<table>
    <tr>
        <td>Language</td>
        <td>Compiler/Runtime</td>
        <td>Build Flags</td>
        <td>Runtime Features</td>
    </tr>
    <tr>
        <td>C</td>
        <td>gcc 12.2.0</td>
        <td><code>-pipe -Wall -O3 -fomit-frame-pointer -march=native -fopenmp</code></td>
        <td>Native execution</td>
    </tr>
    <tr>
        <td>Java</td>
        <td>javac 24.0.1 (GraalVM)</td>
        <td><code>native-image --silent --gc=G1 -cp . -O3 -march=native</code></td>
        <td>Native execution with GraalVM</td>
    </tr>
    <tr>
        <td>JavaScript</td>
        <td>N/A</td>
        <td>N/A</td>
        <td>Deno 2.3.3 (V8 13.7.152.6)</td>
    </tr>
    <tr>
        <td>TypeScript</td>
        <td>N/A</td>
        <td>N/A</td>
        <td>Deno 2.3.3 (TypeScript 5.8.3)</td>
    </tr>
    <tr>
        <td>Ruby</td>
        <td>N/A</td>
        <td>N/A</td>
        <td>Ruby 3.1.2p20 with YJIT</td>
    </tr>
    <tr>
        <td>Zig</td>
        <td>zig 0.14</td>
        <td><code>-O ReleaseFast -lc</code></td>
        <td>Native execution</td>
    </tr>
</table>
</details>

<details><summary><h2>Benchmark-specific dependencies</h2></summary>
<table>
    <tr>
        <td>Benchmark</td>
        <td>C</td>
        <td>Java</td>
        <td>JavaScript/TypeScript</td>
        <td>Ruby</td>
        <td>Zig</td>
    </tr>
    <tr>
        <td>binarytrees</td>
        <td>Standard C library</td>
        <td><code>java.util.concurrent</code></td>
        <td>Deno standard library</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>fannkuchredux</td>
        <td>OpenMP</td>
        <td><code>java.util.concurrent</code></td>
        <td>Deno standard library</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>fasta</td>
        <td>Standard C library</td>
        <td>Java standard library</td>
        <td><code>TextEncoder</code>, Deno I/O APIs</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>knucleotide</td>
        <td>Custom hash table (<code>khash.h</code>), OpenMP</td>
        <td>Java collections, concurrency</td>
        <td><code>TextDecoder</code>, Deno I/O APIs</td>
        <td>Ruby standard library, parallel execution</td>
        <td>Zig standard library, custom Map implementation</td>
    </tr>
    <tr>
        <td>mandelbrot</td>
        <td>OpenMP</td>
        <td><code>java.util.concurrent</code></td>
        <td>Deno I/O APIs, <code>navigator.hardwareConcurrency</code></td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>nbody</td>
        <td>Standard C library, math library</td>
        <td>Java standard library</td>
        <td>Deno standard library</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>pidigits</td>
        <td>GMP library (<code>-lgmp</code>)</td>
        <td><code>java.math.BigInteger</code></td>
        <td>JavaScript BigInt</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>regexredux</td>
        <td>PCRE2 library (<code>-lpcre2-8</code>)</td>
        <td><code>java.util.regex</code>, <code>java.util.concurrent</code></td>
        <td>JavaScript RegExp, Deno I/O APIs</td>
        <td>Ruby Regexp</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>reversecomplement</td>
        <td>Standard C library</td>
        <td>Java standard library</td>
        <td><code>TextDecoder</code>, Deno I/O APIs</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
    <tr>
        <td>spectralnorm</td>
        <td>Standard C library, math library</td>
        <td>Java standard library</td>
        <td>Deno standard library</td>
        <td>Ruby standard library</td>
        <td>Zig standard library</td>
    </tr>
</table>
</details>

## How to run

There are multiple steps needed to run the program.
The `measure_power.py` script is used to measure the power consumption of the program.
But it was created to run while having a Prometheus server running in the background - so that the power consumption can be measured over time.
To get Prometheus to work, please follow the instructions on their [website here](https://prometheus.io/docs/prometheus/latest/installation/).

Please look at [Language Dependencies](#language-dependencies) and [Benchmark-specific dependencies](#benchmark-specific-dependencies) for more information on the dependencies used to run each benchmark.

To run the `measure_power.py` script, run the following commands (we have only run it with Python 3.11):

```bash
python3 -m .venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Then run the script with the following command:

```bash
python3 measure_power.py
```

A csv file will be created named `energy_results.csv`.

Now run the following command to create visualizations, and a LaTeX table of the results:

```bash
python3 visualize.py
```

This will create the following files:

- `build_energy_comparison.png`
- `relative_run_energy.png`
- `run_energy_comparison.png`
- `total_energy_comparison.png`
- `energy_usage_tables.tex`
