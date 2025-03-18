# Ideas

Test DragonflyDB with Redis

- Can be done on a low resource machine (Effectiveness)
- Can be done on a essentially no limit resource machine (Scalability)
- Compare "ideal case (HPC)" with low-performance to see if Redis or Dragonfly can reasonably run on low performance

Data structure comparison

- Fenwick tree vs traditional segment tree - cache misses and locality

Programming language comparison

- Ruby vs Python stdlib (array, sorting) with / without JIT-compilation
- Newer languages:
    - Zig, Rust, Odin, Pony, Some others?
- Energy consumption of popular languages (replicate [recent popular but disputed study](https://haslab.github.io/SAFER/scp21.pdf))

## Benchmarking energy consumption of programming languages

### Overall idea

We will try and replicate the [recent popular but disputed study](https://haslab.github.io/SAFER/scp21.pdf).
It will be difficult to reproduce as the hardware was not specified (we can try to contact the authors).

### Languages

The languages we want to benchmark are:

- Zig
- Rust
- Odin
- Pony
- If wanting to compare we need:
  - C
  - Some other language (e.g. Python, Ruby)

### Benchmarks

The benchmarks we want to run are:

| Benchmark | Description | Input |
| --- | --- | --- |
| n-body | Double precision N-body simulation | 50M |
| fannkuch-redux | Indexed access to tiny integer sequence | 12 |
| spectral-norm | Eigenvalue using the power method | 5,500 |
| mandelbrot | Generate Mandelbrot set portable bitmap file | 16,000 |
| pidigits | Streaming arbitrary precision arithmetic | 10,000 |
| regex-redux | Match DNA 8mers and substitute magic patterns | fasta output |
| fasta | Generate and write random DNA sequences | 25M |
| k-nucleotide | Hashtable update and k-nucleotide strings | fasta output |
| reverse-complement | Read DNA sequences, write their reverse-complement | fasta output |
| binary-trees | Allocate, traverse and deallocate many binary trees | 21 |
| chameneos-redux | Symmetrical thread rendezvous requests | 6M |
| meteor-contest | Search for solutions to shape packing puzzle | 2,098 |
| thread-ring | Switch from thread to thread passing one token | 50M |

### Hardware

It will be important to note the machine we are running on.

### Comparisons

We might be able to compare our results somewhat with the original paper as they Joules per benchmarks have been normalized compared to C.
