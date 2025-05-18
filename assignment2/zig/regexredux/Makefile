build:
	zig build-exe -O ReleaseFast regexredux.zig -lc -lpcre -I/opt/homebrew/include -L/opt/homebrew/lib

run: build
	./regexredux < ../../input/regexredux-input5000000.txt

clean:
	rm -f regexredux
	rm -f regexredux.o
