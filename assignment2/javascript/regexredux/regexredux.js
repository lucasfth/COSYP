// The Computer Language Benchmarks Game
// http://benchmarksgame.alioth.debian.org/
//
// regex-dna program contributed by Jesse Millikan
// Base on the Ruby version by jose fco. gonzalez
// fixed by Matthew Wilson
// ported to Node.js and sped up by Roman Pletnev
// converted from regex-dna program
// Modified for Deno compatibility

// DENO MODIFICATION: Replace Node.js file reading with Deno's API
async function main() {
  // Read input data
  const decoder = new TextDecoder("ascii");
  const buffer = new Uint8Array(1024 * 1024); // 1MB buffer
  let i = "";

  while (true) {
    const readResult = await Deno.stdin.read(buffer);
    if (readResult === null) break;
    i += decoder.decode(buffer.subarray(0, readResult), { stream: true });
  }

  // Original code starts here
  const ilen = i.length;
  let clen, j;
  const q = [
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

  const b = [
    "-",
    /\|[^|][^|]*\|/g,
    "|",
    /<[^>]*>/g,
    "<2>",
    /a[NSt]|BY/g,
    "<3>",
    /aND|caN|Ha[DS]|WaS/g,
    "<4>",
    /tHa[Nt]/g,
  ];

  i = i.replace(/^>.*\n|\n/gm, "");
  clen = i.length;
  for (j = 0; j < q.length; ++j) {
    const qj = q[j],
      m = i.match(qj);
    console.log(qj.source, m ? m.length : 0);
  }

  while (b.length) i = i.replace(b.pop(), b.pop());
  console.log(["", ilen, clen, i.length].join("\n"));
}

// DENO MODIFICATION: Run the main function
main().catch((err) => {
  console.error("Error:", err);
  Deno.exit(1);
});
