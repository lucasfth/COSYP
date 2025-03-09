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
		./build/count-then-move 1 8 16777216 metrics.csv 0; \
		./build/count-then-move 2 8 16777216 metrics.csv 0; \
		./build/count-then-move 4 8 16777216 metrics.csv 0; \
		./build/count-then-move 8 8 16777216 metrics.csv 0; \
		./build/count-then-move 16 8 16777216 metrics.csv 0; \
		./build/count-then-move 32 8 16777216 metrics.csv 0; \
		./build/count-then-move 8 1 16777216 metrics.csv 0; \
		./build/count-then-move 8 2 16777216 metrics.csv 0; \
		./build/count-then-move 8 4 16777216 metrics.csv 0; \
		./build/count-then-move 8 8 16777216 metrics.csv 0; \
		./build/count-then-move 8 8 4096 metrics.csv 0; \
		./build/count-then-move 8 8 65536 metrics.csv 0; \
		./build/count-then-move 8 8 1048576 metrics.csv 0; \
		./build/count-then-move 8 8 67108864 metrics.csv 0; \
	done

run-concurrent-output: build
	@echo "Running concurrent-output with different parameters"
	@for i in 1 2 3; do \
		./build/concurrent-output 1 8 16777216 metrics.csv 0; \
		./build/concurrent-output 2 8 16777216 metrics.csv 0; \
		./build/concurrent-output 4 8 16777216 metrics.csv 0; \
		./build/concurrent-output 8 8 16777216 metrics.csv 0; \
		./build/concurrent-output 16 8 16777216 metrics.csv 0; \
		./build/concurrent-output 32 8 16777216 metrics.csv 0; \
		./build/concurrent-output 8 1 16777216 metrics.csv 0; \
		./build/concurrent-output 8 2 16777216 metrics.csv 0; \
		./build/concurrent-output 8 4 16777216 metrics.csv 0; \
		./build/concurrent-output 8 8 16777216 metrics.csv 0; \
		./build/concurrent-output 8 8 4096 metrics.csv 0; \
		./build/concurrent-output 8 8 65536 metrics.csv 0; \
		./build/concurrent-output 8 8 1048576 metrics.csv 0; \
		./build/concurrent-output 8 8 67108864 metrics.csv 0; \
	done

run-all: build
	@echo "Running count-then-move and concurrent-output with different parameters"
	@$(MAKE) run-count-then-move
	@$(MAKE) run-concurrent-output

# Declare phony targets to avoid conflicts with files of the same name
.PHONY: all configure build clean
