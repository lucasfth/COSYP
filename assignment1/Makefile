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
	@for i in 1 2 3 4 5; do \
		./build/count-then-move 8 8 16777216 metrics.csv 0; \
		./build/count-then-move 4 8 16777216 metrics.csv 0; \
		./build/count-then-move 8 4 16777216 metrics.csv 0; \
		./build/count-then-move 8 8 8388608 metrics.csv 0; \
		./build/count-then-move 8 8 16777216 metrics.csv 0; \

# Declare phony targets to avoid conflicts with files of the same name
.PHONY: all configure build clean
