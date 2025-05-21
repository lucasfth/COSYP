/* https://github.com/greensoftwarelab/Energy-Languages/blob/master/JavaScript/mandelbrot/mandelbrot.node

   The Computer Language Benchmarks Game
   http://benchmarksgame.alioth.debian.org/

   contributed by Andreas Schmelz 2016-02-14
   adapted for Deno by GitHub Copilot 2025
*/

/*
Modified for Deno compatibility and performance improvements.
*/

// Get the number of available CPU cores
const cpuCores = navigator.hardwareConcurrency || 4;
let numCPUs = cpuCores * 2;

// Parse dimension from command line arguments
const d = parseInt(Deno.args[0]) || 200;

// Validate input dimension
if (d % 8 != 0) {
  console.error("d must be multiple of 8");
  Deno.exit(-1);
}

// Ensure even distribution of work across CPUs
while (((d * d) / numCPUs) % 8 != 0) {
  numCPUs--;
}

/**
 * Main function to run Mandelbrot calculation using multiple processes
 */
async function main() {
  // Output header for PBM format
  const textEncoder = new TextEncoder();
  const header = `P4\n${d} ${d}\n`;
  await Deno.stdout.write(textEncoder.encode(header));

  const processes = [];
  const outputs = [];

  // Spawn worker processes for parallel computation
  for (let i = 0; i < numCPUs; i++) {
    const start = Math.floor((i * d) / numCPUs);
    const end = Math.floor(((i + 1) * d) / numCPUs);

    // Run worker process
    const process = Deno.run({
      cmd: [
        "deno",
        "run",
        "--allow-read",
        "--allow-write",
        "worker.js",
        d.toString(),
        start.toString(),
        end.toString(),
        (i + 1).toString(),
      ],
      stdout: "piped",
      stderr: "piped",
    });

    processes.push(process);
  }

  // Collect and process outputs
  for (const process of processes) {
    const output = await process.output();
    await Deno.stdout.write(output);

    // Close the process resources
    process.close();
  }
}

/**
 * Calculate the mandelbrot set value at a specific point
 * @param {number} Cr - Real part of complex number
 * @param {number} Ci - Imaginary part of complex number
 * @return {number} Squared magnitude
 */
function doCalc(Cr, Ci) {
  let Zr = 0,
    Zi = 0,
    Tr = 0,
    Ti = 0;
  const iter = 50;
  const limit = 4;

  for (let i = 0; i < iter && Tr + Ti <= limit; i++) {
    Zi = 2 * Zr * Zi + Ci;
    Zr = Tr - Ti + Cr;
    Tr = Zr * Zr;
    Ti = Zi * Zi;
  }
  return Tr + Ti;
}

// Start the application
main();
