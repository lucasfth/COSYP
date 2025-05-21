// Worker process for Mandelbrot calculation

// Get worker parameters from arguments
const args = Deno.args;
const d = parseInt(args[0]);
const start = parseInt(args[1]);
const end = parseInt(args[2]);
const workerId = parseInt(args[3]);

const iter = 50;
const limit = 4;

// Calculate the portion of the Mandelbrot set
let byte_acc = 0;
let bit_num = 0;
let buff = new Uint8Array(Math.floor(((d * d) / 8 / (end - start)) * d));

function doCalc(Cr, Ci) {
  let Zr = 0,
    Zi = 0,
    Tr = 0,
    Ti = 0;
  for (let i = 0; i < iter && Tr + Ti <= limit; i++) {
    Zi = 2 * Zr * Zi + Ci;
    Zr = Tr - Ti + Cr;
    Tr = Zr * Zr;
    Ti = Zi * Zi;
  }
  return Tr + Ti;
}

// Calculate the mandelbrot set portion
const xd = 2 / d;
let it = 0;
for (let y = start; y < end; y++) {
  const yd = (2 * y) / d - 1;
  for (let x = 0; x < d; x++) {
    const sum = doCalc(xd * x - 1.5, yd);

    byte_acc |= sum <= limit ? 1 : 0;
    bit_num++;

    if (bit_num === 8) {
      buff[it++] = byte_acc;
      byte_acc = 0;
      bit_num = 0;
    } else {
      byte_acc <<= 1;
    }
  }
}

// Write the result directly to stdout as binary
await Deno.stdout.write(buff);
