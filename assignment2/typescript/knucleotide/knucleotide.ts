/* https://github.com/greensoftwarelab/Energy-Languages/blob/master/TypeScript/k-nucleotide/knucleotide.ts

   The Computer Language Benchmarks Game
   http://benchmarksgame.alioth.debian.org/

   contributed by Josh Goldfoot
   modified to support Deno
*/

/// <reference path="../node_modules/@types/node/index.d.ts" />

import { createInterface } from "node:readline";

class RefNum {
  num: number;
  constructor(n: number) {
    this.num = n;
  }
}

function frequency(sequence: string, length: number): Map<string, RefNum> {
  var freq = new Map<string, RefNum>();
  var n = sequence.length - length + 1;
  var sub = "";
  var m: RefNum;
  for (var i = 0; i < n; i++) {
    sub = sequence.substr(i, length);
    m = freq.get(sub);
    if (m === undefined) {
      freq.set(sub, new RefNum(1));
    } else {
      m.num += 1;
    }
  }
  return freq;
}

function sort(sequence: string, length: number): void {
  var freq = frequency(sequence, length);
  var keys = new Array<string>();
  for (let k of freq.keys()) keys.push(k);
  keys.sort((a, b) => freq.get(b).num - freq.get(a).num);
  var n = sequence.length - length + 1;
  keys.forEach((key) => {
    var count = ((freq.get(key).num * 100) / n).toFixed(3);
    console.log(key + " " + count);
  });
  console.log("");
}

function find(haystack: string, needle: string): void {
  var freq = frequency(haystack, needle.length);
  var m = freq.get(needle);
  var num = m ? m.num : 0;
  console.log(num + "\t" + needle);
}

async function main() {
  var sequence = "";
  var reading = false;

  // Read the entire input as text
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
  for (const line of lines) {
    if (reading) {
      if (line[0] !== ">") {
        sequence += line.toUpperCase();
      }
    } else {
      reading = line.substr(0, 6) === ">THREE";
    }
  }

  // Run the analysis
  sort(sequence, 1);
  sort(sequence, 2);
  find(sequence, "GGT");
  find(sequence, "GGTA");
  find(sequence, "GGTATT");
  find(sequence, "GGTATTTTAATT");
  find(sequence, "GGTATTTTAATTTATAGT");
}

main();
