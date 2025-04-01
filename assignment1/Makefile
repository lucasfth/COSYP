# Default target: build the project using CMake
all: build

# Target to configure the project with CMake
configure:
	mkdir -p build
	cd build && cmake ..

# Target to build the project
build: configure
	cd build && make

# Target to clean the build files
clean:
	rm -rf build

# Run the count-then-move program with different parameters and repeat each run five times
run-count-then-move: build
	@echo "Running count-then-move with different parameters"
	@for i in 1 2 3; do \
		./build/count-then-move 1 1 16777216 metrics.csv 0; \
		./build/count-then-move 2 1 16777216 metrics.csv 0; \
		./build/count-then-move 4 1 16777216 metrics.csv 0; \
		./build/count-then-move 8 1 16777216 metrics.csv 0; \
		./build/count-then-move 16 1 16777216 metrics.csv 0; \
		./build/count-then-move 32 1 16777216 metrics.csv 0; \
		./build/count-then-move 1 2 16777216 metrics.csv 0; \
		./build/count-then-move 2 2 16777216 metrics.csv 0; \
		./build/count-then-move 4 2 16777216 metrics.csv 0; \
		./build/count-then-move 8 2 16777216 metrics.csv 0; \
		./build/count-then-move 16 2 16777216 metrics.csv 0; \
		./build/count-then-move 32 2 16777216 metrics.csv 0; \
		./build/count-then-move 1 3 16777216 metrics.csv 0; \
		./build/count-then-move 2 3 16777216 metrics.csv 0; \
		./build/count-then-move 4 3 16777216 metrics.csv 0; \
		./build/count-then-move 8 3 16777216 metrics.csv 0; \
		./build/count-then-move 16 3 16777216 metrics.csv 0; \
		./build/count-then-move 32 3 16777216 metrics.csv 0; \
		./build/count-then-move 1 4 16777216 metrics.csv 0; \
		./build/count-then-move 2 4 16777216 metrics.csv 0; \
		./build/count-then-move 4 4 16777216 metrics.csv 0; \
		./build/count-then-move 8 4 16777216 metrics.csv 0; \
		./build/count-then-move 16 4 16777216 metrics.csv 0; \
		./build/count-then-move 32 4 16777216 metrics.csv 0; \
		./build/count-then-move 1 5 16777216 metrics.csv 0; \
		./build/count-then-move 2 5 16777216 metrics.csv 0; \
		./build/count-then-move 4 5 16777216 metrics.csv 0; \
		./build/count-then-move 8 5 16777216 metrics.csv 0; \
		./build/count-then-move 16 5 16777216 metrics.csv 0; \
		./build/count-then-move 32 5 16777216 metrics.csv 0; \
		./build/count-then-move 1 6 16777216 metrics.csv 0; \
		./build/count-then-move 2 6 16777216 metrics.csv 0; \
		./build/count-then-move 4 6 16777216 metrics.csv 0; \
		./build/count-then-move 8 6 16777216 metrics.csv 0; \
		./build/count-then-move 16 6 16777216 metrics.csv 0; \
		./build/count-then-move 32 6 16777216 metrics.csv 0; \
		./build/count-then-move 1 7 16777216 metrics.csv 0; \
		./build/count-then-move 2 7 16777216 metrics.csv 0; \
		./build/count-then-move 4 7 16777216 metrics.csv 0; \
		./build/count-then-move 8 7 16777216 metrics.csv 0; \
		./build/count-then-move 16 7 16777216 metrics.csv 0; \
		./build/count-then-move 32 7 16777216 metrics.csv 0; \
		./build/count-then-move 1 8 16777216 metrics.csv 0; \
		./build/count-then-move 2 8 16777216 metrics.csv 0; \
		./build/count-then-move 4 8 16777216 metrics.csv 0; \
		./build/count-then-move 8 8 16777216 metrics.csv 0; \
		./build/count-then-move 16 8 16777216 metrics.csv 0; \
		./build/count-then-move 32 8 16777216 metrics.csv 0; \
		./build/count-then-move 1 9 16777216 metrics.csv 0; \
		./build/count-then-move 2 9 16777216 metrics.csv 0; \
		./build/count-then-move 4 9 16777216 metrics.csv 0; \
		./build/count-then-move 8 9 16777216 metrics.csv 0; \
		./build/count-then-move 16 9 16777216 metrics.csv 0; \
		./build/count-then-move 32 9 16777216 metrics.csv 0; \
		./build/count-then-move 1 10 16777216 metrics.csv 0; \
		./build/count-then-move 2 10 16777216 metrics.csv 0; \
		./build/count-then-move 4 10 16777216 metrics.csv 0; \
		./build/count-then-move 8 10 16777216 metrics.csv 0; \
		./build/count-then-move 16 10 16777216 metrics.csv 0; \
		./build/count-then-move 32 10 16777216 metrics.csv 0; \
		./build/count-then-move 1 11 16777216 metrics.csv 0; \
		./build/count-then-move 2 11 16777216 metrics.csv 0; \
		./build/count-then-move 4 11 16777216 metrics.csv 0; \
		./build/count-then-move 8 11 16777216 metrics.csv 0; \
		./build/count-then-move 16 11 16777216 metrics.csv 0; \
		./build/count-then-move 32 11 16777216 metrics.csv 0; \
		./build/count-then-move 1 12 16777216 metrics.csv 0; \
		./build/count-then-move 2 12 16777216 metrics.csv 0; \
		./build/count-then-move 4 12 16777216 metrics.csv 0; \
		./build/count-then-move 8 12 16777216 metrics.csv 0; \
		./build/count-then-move 16 12 16777216 metrics.csv 0; \
		./build/count-then-move 32 12 16777216 metrics.csv 0; \
		./build/count-then-move 1 13 16777216 metrics.csv 0; \
		./build/count-then-move 2 13 16777216 metrics.csv 0; \
		./build/count-then-move 4 13 16777216 metrics.csv 0; \
		./build/count-then-move 8 13 16777216 metrics.csv 0; \
		./build/count-then-move 16 13 16777216 metrics.csv 0; \
		./build/count-then-move 32 13 16777216 metrics.csv 0; \
		./build/count-then-move 1 14 16777216 metrics.csv 0; \
		./build/count-then-move 2 14 16777216 metrics.csv 0; \
		./build/count-then-move 4 14 16777216 metrics.csv 0; \
		./build/count-then-move 8 14 16777216 metrics.csv 0; \
		./build/count-then-move 16 14 16777216 metrics.csv 0; \
		./build/count-then-move 32 14 16777216 metrics.csv 0; \
		./build/count-then-move 1 15 16777216 metrics.csv 0; \
		./build/count-then-move 2 15 16777216 metrics.csv 0; \
		./build/count-then-move 4 15 16777216 metrics.csv 0; \
		./build/count-then-move 8 15 16777216 metrics.csv 0; \
		./build/count-then-move 16 15 16777216 metrics.csv 0; \
		./build/count-then-move 32 15 16777216 metrics.csv 0; \
		./build/count-then-move 1 16 16777216 metrics.csv 0; \
		./build/count-then-move 2 16 16777216 metrics.csv 0; \
		./build/count-then-move 4 16 16777216 metrics.csv 0; \
		./build/count-then-move 8 16 16777216 metrics.csv 0; \
		./build/count-then-move 16 16 16777216 metrics.csv 0; \
		./build/count-then-move 32 16 16777216 metrics.csv 0; \
		./build/count-then-move 1 17 16777216 metrics.csv 0; \
		./build/count-then-move 2 17 16777216 metrics.csv 0; \
		./build/count-then-move 4 17 16777216 metrics.csv 0; \
		./build/count-then-move 8 17 16777216 metrics.csv 0; \
		./build/count-then-move 16 17 16777216 metrics.csv 0; \
		./build/count-then-move 32 17 16777216 metrics.csv 0; \
		./build/count-then-move 1 18 16777216 metrics.csv 0; \
		./build/count-then-move 2 18 16777216 metrics.csv 0; \
		./build/count-then-move 4 18 16777216 metrics.csv 0; \
		./build/count-then-move 8 18 16777216 metrics.csv 0; \
		./build/count-then-move 16 18 16777216 metrics.csv 0; \
		./build/count-then-move 32 18 16777216 metrics.csv 0; \
	done

run-concurrent-output: build
	@echo "Running concurrent-output with different parameters"
	@for i in 1 2 3; do \
		./build/concurrent-output 1 1 16777216 metrics.csv 0; \
		./build/concurrent-output 2 1 16777216 metrics.csv 0; \
		./build/concurrent-output 4 1 16777216 metrics.csv 0; \
		./build/concurrent-output 8 1 16777216 metrics.csv 0; \
		./build/concurrent-output 16 1 16777216 metrics.csv 0; \
		./build/concurrent-output 32 1 16777216 metrics.csv 0; \
		./build/concurrent-output 1 2 16777216 metrics.csv 0; \
		./build/concurrent-output 2 2 16777216 metrics.csv 0; \
		./build/concurrent-output 4 2 16777216 metrics.csv 0; \
		./build/concurrent-output 8 2 16777216 metrics.csv 0; \
		./build/concurrent-output 16 2 16777216 metrics.csv 0; \
		./build/concurrent-output 32 2 16777216 metrics.csv 0; \
		./build/concurrent-output 1 3 16777216 metrics.csv 0; \
		./build/concurrent-output 2 3 16777216 metrics.csv 0; \
		./build/concurrent-output 4 3 16777216 metrics.csv 0; \
		./build/concurrent-output 8 3 16777216 metrics.csv 0; \
		./build/concurrent-output 16 3 16777216 metrics.csv 0; \
		./build/concurrent-output 32 3 16777216 metrics.csv 0; \
		./build/concurrent-output 1 4 16777216 metrics.csv 0; \
		./build/concurrent-output 2 4 16777216 metrics.csv 0; \
		./build/concurrent-output 4 4 16777216 metrics.csv 0; \
		./build/concurrent-output 8 4 16777216 metrics.csv 0; \
		./build/concurrent-output 16 4 16777216 metrics.csv 0; \
		./build/concurrent-output 32 4 16777216 metrics.csv 0; \
		./build/concurrent-output 1 5 16777216 metrics.csv 0; \
		./build/concurrent-output 2 5 16777216 metrics.csv 0; \
		./build/concurrent-output 4 5 16777216 metrics.csv 0; \
		./build/concurrent-output 8 5 16777216 metrics.csv 0; \
		./build/concurrent-output 16 5 16777216 metrics.csv 0; \
		./build/concurrent-output 32 5 16777216 metrics.csv 0; \
		./build/concurrent-output 1 6 16777216 metrics.csv 0; \
		./build/concurrent-output 2 6 16777216 metrics.csv 0; \
		./build/concurrent-output 4 6 16777216 metrics.csv 0; \
		./build/concurrent-output 8 6 16777216 metrics.csv 0; \
		./build/concurrent-output 16 6 16777216 metrics.csv 0; \
		./build/concurrent-output 32 6 16777216 metrics.csv 0; \
		./build/concurrent-output 1 7 16777216 metrics.csv 0; \
		./build/concurrent-output 2 7 16777216 metrics.csv 0; \
		./build/concurrent-output 4 7 16777216 metrics.csv 0; \
		./build/concurrent-output 8 7 16777216 metrics.csv 0; \
		./build/concurrent-output 16 7 16777216 metrics.csv 0; \
		./build/concurrent-output 32 7 16777216 metrics.csv 0; \
		./build/concurrent-output 1 8 16777216 metrics.csv 0; \
		./build/concurrent-output 2 8 16777216 metrics.csv 0; \
		./build/concurrent-output 4 8 16777216 metrics.csv 0; \
		./build/concurrent-output 8 8 16777216 metrics.csv 0; \
		./build/concurrent-output 16 8 16777216 metrics.csv 0; \
		./build/concurrent-output 32 8 16777216 metrics.csv 0; \
		./build/concurrent-output 1 9 16777216 metrics.csv 0; \
		./build/concurrent-output 2 9 16777216 metrics.csv 0; \
		./build/concurrent-output 4 9 16777216 metrics.csv 0; \
		./build/concurrent-output 8 9 16777216 metrics.csv 0; \
		./build/concurrent-output 16 9 16777216 metrics.csv 0; \
		./build/concurrent-output 32 9 16777216 metrics.csv 0; \
		./build/concurrent-output 1 10 16777216 metrics.csv 0; \
		./build/concurrent-output 2 10 16777216 metrics.csv 0; \
		./build/concurrent-output 4 10 16777216 metrics.csv 0; \
		./build/concurrent-output 8 10 16777216 metrics.csv 0; \
		./build/concurrent-output 16 10 16777216 metrics.csv 0; \
		./build/concurrent-output 32 10 16777216 metrics.csv 0; \
		./build/concurrent-output 1 11 16777216 metrics.csv 0; \
		./build/concurrent-output 2 11 16777216 metrics.csv 0; \
		./build/concurrent-output 4 11 16777216 metrics.csv 0; \
		./build/concurrent-output 8 11 16777216 metrics.csv 0; \
		./build/concurrent-output 16 11 16777216 metrics.csv 0; \
		./build/concurrent-output 32 11 16777216 metrics.csv 0; \
		./build/concurrent-output 1 12 16777216 metrics.csv 0; \
		./build/concurrent-output 2 12 16777216 metrics.csv 0; \
		./build/concurrent-output 4 12 16777216 metrics.csv 0; \
		./build/concurrent-output 8 12 16777216 metrics.csv 0; \
		./build/concurrent-output 16 12 16777216 metrics.csv 0; \
		./build/concurrent-output 32 12 16777216 metrics.csv 0; \
		./build/concurrent-output 1 13 16777216 metrics.csv 0; \
		./build/concurrent-output 2 13 16777216 metrics.csv 0; \
		./build/concurrent-output 4 13 16777216 metrics.csv 0; \
		./build/concurrent-output 8 13 16777216 metrics.csv 0; \
		./build/concurrent-output 16 13 16777216 metrics.csv 0; \
		./build/concurrent-output 32 13 16777216 metrics.csv 0; \
		./build/concurrent-output 1 14 16777216 metrics.csv 0; \
		./build/concurrent-output 2 14 16777216 metrics.csv 0; \
		./build/concurrent-output 4 14 16777216 metrics.csv 0; \
		./build/concurrent-output 8 14 16777216 metrics.csv 0; \
		./build/concurrent-output 16 14 16777216 metrics.csv 0; \
		./build/concurrent-output 32 14 16777216 metrics.csv 0; \
		./build/concurrent-output 1 15 16777216 metrics.csv 0; \
		./build/concurrent-output 2 15 16777216 metrics.csv 0; \
		./build/concurrent-output 4 15 16777216 metrics.csv 0; \
		./build/concurrent-output 8 15 16777216 metrics.csv 0; \
		./build/concurrent-output 16 15 16777216 metrics.csv 0; \
		./build/concurrent-output 32 15 16777216 metrics.csv 0; \
		./build/concurrent-output 1 16 16777216 metrics.csv 0; \
		./build/concurrent-output 2 16 16777216 metrics.csv 0; \
		./build/concurrent-output 4 16 16777216 metrics.csv 0; \
		./build/concurrent-output 8 16 16777216 metrics.csv 0; \
		./build/concurrent-output 16 16 16777216 metrics.csv 0; \
		./build/concurrent-output 32 16 16777216 metrics.csv 0; \
		./build/concurrent-output 1 17 16777216 metrics.csv 0; \
		./build/concurrent-output 2 17 16777216 metrics.csv 0; \
		./build/concurrent-output 4 17 16777216 metrics.csv 0; \
		./build/concurrent-output 8 17 16777216 metrics.csv 0; \
		./build/concurrent-output 16 17 16777216 metrics.csv 0; \
		./build/concurrent-output 32 17 16777216 metrics.csv 0; \
		./build/concurrent-output 1 18 16777216 metrics.csv 0; \
		./build/concurrent-output 2 18 16777216 metrics.csv 0; \
		./build/concurrent-output 4 18 16777216 metrics.csv 0; \
		./build/concurrent-output 8 18 16777216 metrics.csv 0; \
		./build/concurrent-output 16 18 16777216 metrics.csv 0; \
		./build/concurrent-output 32 18 16777216 metrics.csv 0; \
	done

perf-count-then-move: build
	@echo "Running perf on count then move with different parameters"
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-1-18.txt ./build/count-then-move 1 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-2-18.txt ./build/count-then-move 2 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-4-18.txt ./build/count-then-move 4 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-8-18.txt ./build/count-then-move 8 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-16-18.txt ./build/count-then-move 16 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-32-18.txt ./build/count-then-move 32 18 16777216 metrics.csv 0; \

perf-concurrent-output: build
	@echo "Running perf on concurrent-output with different parameters"
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-1-18.txt ./build/concurrent-output 1 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-2-18.txt ./build/concurrent-output 2 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-4-18.txt ./build/concurrent-output 4 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-8-18.txt ./build/concurrent-output 8 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-16-18.txt ./build/concurrent-output 16 18 16777216 metrics.csv 0; \
	perf stat -e LLC-load-misses,LLC-store-misses -o perf-ctm-32-18.txt ./build/concurrent-output 32 18 16777216 metrics.csv 0; \

run-all: build
	@echo "Running count-then-move and concurrent-output with different parameters"
	@$(MAKE) run-count-then-move
	@$(MAKE) run-concurrent-output

perf-all: build
	@echo "Running perf on count-then-move and concurrent-output with different parameters"
	@$(MAKE) perf-count-then-move
	@$(MAKE) perf-concurrent-output

# Declare phony targets to avoid conflicts with files of the same name
.PHONY: all configure build clean
