/* https://github.com/greensoftwarelab/Energy-Languages/blob/master/JavaScript/fannkuch-redux/fannkuchredux.node-4.node

   The Computer Language Benchmarks Game
   http://benchmarksgame.alioth.debian.org/

   contributed by Isaac Gouy, transliterated from Mike Pall's Lua program 
   modified by Roman Pletnev
*/

function fannkuch(n) {
   var p = [], q = [], s = [];
   var sign = 1, maxflips = 0, sum = 0, m = n-1;
   for(var i=0; i<n; i++){ p.push(i); q.push(i); s.push(i); }
   do {
      // Copy and flip.
      var q0 = p[0];                                     // Cache 0th element.
      if (q0 != 0){
         for(var i=1; i<n; i++) q[i] = p[i];             // Work on a copy.
         var flips = 1;
         do { 
            var qq = q[q0]; 
            if (qq === 0){                               // ... until 0th element is 0.
               sum += sign*flips;
	       if (flips > maxflips) maxflips = flips;   // New maximum?
               break; 
            } 
 	    q[q0] = q0; 
	    if (q0 >= 3){
	       var i = 1, j = q0 - 1, t;
               do { t = q[i]; q[i] = q[j]; q[j] = t; i++; j--; } while (i < j); 
            }
	    q0 = qq; flips++;
         } while (true); 
      }
      // Permute.
      if (sign === 1){
         var t = p[1]; p[1] = p[0]; p[0] = t; sign = -1; // Rotate 0<-1.
      } else { 
         var t = p[1]; p[1] = p[2]; p[2] = t; sign = 1;  // Rotate 0<-1 and 0<-1<-2.
         for(var i=2; i<n; i++){ 
	    var sx = s[i];
	    if (sx != 0){ s[i] = sx-1; break; }
	    if (i === m) return [sum,maxflips];      // Out of permutations.
	    s[i] = i;
	    // Rotate 0<-...<-i+1.
	    t = p[0]; for(var j=0; j<=i; j++){ p[j] = p[j+1]; } p[i+1] = t;
         }
      }
   } while (true);
}

var n = +process.argv[2];
var pf = fannkuch(n);
console.log(pf[0] + "\n" + "Pfannkuchen(" + n + ") = " + pf[1]);