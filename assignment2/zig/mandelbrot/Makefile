build:
	zig build-exe -O ReleaseFast mandelbrot.zig -lc

run: build
	./mandelbrot 16000

clean:
	rm -f mandelbrot
	rm -f mandelbrot.o
