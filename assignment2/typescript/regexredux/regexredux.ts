/* https://github.com/greensoftwarelab/Energy-Languages/blob/master/TypeScript/regex-redux/regexredux.typescript-3.ts

   The Computer Language Benchmarks Game
   http://benchmarksgame.alioth.debian.org/

   by Josh Goldfoot, adapted from the node.js version
   Modified for Deno compatibility
*/

// DENO MODIFICATION: Remove Node.js references and imports
// /// <reference path="../node_modules/@types/node/index.d.ts" />
// var fs = require("fs");

// DENO MODIFICATION: Read from stdin using Deno API
async function main() {
  // Read the input data
  const decoder = new TextDecoder("ascii");
  const buffer = new Uint8Array(1024 * 1024); // 1MB buffer
  let i = "";

  while (true) {
    const readResult = await Deno.stdin.read(buffer);
    if (readResult === null) break;
    i += decoder.decode(buffer.subarray(0, readResult), { stream: true });
  }

  // Process the input
  const ilen = i.length;
  i = i.replace(/^>.*\n|\n/gm, "");
  const clen = i.length;

  const iubReplaceLen: Promise<number> = new Promise<number>((resolve) => {
    const iub: string[] = ["-", "|", "<2>", "<3>", "<4>"];
    const iubR: RegExp[] = [
      /\|[^|][^|]*\|/g,
      /<[^>]*>/g,
      /a[NSt]|BY/g,
      /aND|caN|Ha[DS]|WaS/g,
      /tHa[Nt]/g,
    ];
    let seq = i + "";
    while (iub.length) seq = seq.replace(iubR.pop()!, iub.pop()!);
    resolve(seq.length);
  });

  const q: RegExp[] = [
    /agggtaaa|tttaccct/gi,
    /[cgt]gggtaaa|tttaccc[acg]/gi,
    /a[act]ggtaaa|tttacc[agt]t/gi,
    /ag[act]gtaaa|tttac[agt]ct/gi,
    /agg[act]taaa|ttta[agt]cct/gi,
    /aggg[acg]aaa|ttt[cgt]ccct/gi,
    /agggt[cgt]aa|tt[acg]accct/gi,
    /agggta[cgt]a|t[acg]taccct/gi,
    /agggtaa[cgt]|[acg]ttaccct/gi,
  ];

  const promises: Promise<string>[] = q.map(
    (r) =>
      new Promise<string>((resolve) => {
        const m: RegExpMatchArray | null = i.match(r);
        resolve(r.source + " " + (m ? m.length : 0));
      })
  );

  // Output results
  for (let count = 0; count < promises.length; count++)
    console.log(await promises[count]);

  console.log();
  console.log(ilen);
  console.log(clen);
  console.log(await iubReplaceLen);
}

// DENO MODIFICATION: Call the main function with error handling
main().catch((err) => {
  console.error("Error:", err);
  Deno.exit(1);
});
