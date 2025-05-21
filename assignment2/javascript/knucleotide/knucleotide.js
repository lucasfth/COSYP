/* https://github.com/greensoftwarelab/Energy-Languages/blob/master/JavaScript/k-nucleotide/knucleotide.node-2.node

   The Computer Language Benchmarks Game
   http://benchmarksgame.alioth.debian.org/

   Contributed by Jesse Millikan
   Modified by Matt Baker
   Ported, modified, and parallelized by Roman Pletnev
   Modified for Deno compatibility
*/

"use strict";

// DENO MODIFICATION: Remove require statements
// var rd = require("readline"),
//  cp = require("child_process");

function RefNum(num) {
  this.num = num;
}
RefNum.prototype.toString = function () {
  return this.num.toString();
};

function frequency(seq, length) {
  var freq = new Map(),
    n = seq.length - length + 1,
    key,
    cur,
    i = 0;
  for (; i < n; ++i) {
    key = seq.substr(i, length);
    cur = freq.get(key);
    cur === undefined ? freq.set(key, new RefNum(1)) : ++cur.num;
  }
  return freq;
}

function sort(seq, length) {
  var f = frequency(seq, length),
    keys = Array.from(f.keys()),
    n = seq.length - length + 1,
    res = "";
  keys.sort((a, b) => f.get(b).num - f.get(a).num);
  for (var key of keys)
    res +=
      key.toUpperCase() + " " + ((f.get(key).num * 100) / n).toFixed(3) + "\n";
  res += "\n";
  return res;
}

function find(seq, s) {
  var f = frequency(seq, s.length);
  var count = f.get(s);
  return (count ? count.num : 0) + "\t" + s.toUpperCase() + "\n";
}

// DENO MODIFICATION: Replace worker/master with single-threaded implementation
async function main() {
  // Read the entire input
  const decoder = new TextDecoder();
  const buffer = new Uint8Array(1024);
  let input = "";

  while (true) {
    const readResult = await Deno.stdin.read(buffer);
    if (readResult === null) break;
    input += decoder.decode(buffer.subarray(0, readResult), { stream: true });
  }

  // Process the input line by line
  const lines = input.split("\n");
  let seq = "";
  let reading = false;

  for (const line of lines) {
    if (reading) {
      if (line[0] !== ">") {
        seq += line;
      }
    } else {
      reading = line.substr(0, 6) === ">THREE";
    }
  }

  // Run all analyses in sequence (no parallelism)
  let results = "";

  // Tasks from worker 1
  results += sort(seq, 1);
  results += sort(seq, 2);
  results += find(seq, "ggt");

  // Tasks from worker 2
  results += find(seq, "ggta");
  results += find(seq, "ggtatt");

  // Tasks from worker 3
  results += find(seq, "ggtattttaatt");

  // Tasks from worker 4
  results += find(seq, "ggtattttaatttatagt");

  // Output the results
  console.log(results);
}

// DENO MODIFICATION: Call main instead of determining worker vs master
main().catch((err) => {
  console.error("Error:", err);
  Deno.exit(1);
});
