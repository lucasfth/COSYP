build:
	zig build-exe -O ReleaseFast knucleotide.zig

run: build
	./knucleotide < ../../input/knucleotide-input25000000.txt

clean:
	rm -f knucleotide
	rm -f knucleotide.o
	