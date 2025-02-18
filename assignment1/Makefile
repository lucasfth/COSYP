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

# Declare phony targets to avoid conflicts with files of the same name
.PHONY: all configure build clean
