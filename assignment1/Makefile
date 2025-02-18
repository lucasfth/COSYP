# Specify the C++ compiler
COMPILER = g++

# Compiler flags
COMPILER_FLAGS = -std=c++11 -pthread

# Name of the executables to be created
EXECUTABLE_1 = count-then-move
EXECUTABLE_2 = parallel-buffer

# List of source files for each executable
SOURCE_FILES_1 = count-then-move.cpp
SOURCE_FILES_2 = parallel-buffer.cpp

# List of object files (generated from source files)
OBJECT_FILES_1 = $(SOURCE_FILES_1:.cpp=.o)
OBJECT_FILES_2 = $(SOURCE_FILES_2:.cpp=.o)

# Default target: build both executables
all: $(EXECUTABLE_1) $(EXECUTABLE_2)

# Rule to link the object files into the first executable
$(EXECUTABLE_1): $(OBJECT_FILES_1)
	$(COMPILER) $(COMPILER_FLAGS) -o $(EXECUTABLE_1) $(OBJECT_FILES_1)
	rm -f $(OBJECT_FILES_1)  # Remove object files after creating the executable

# Rule to link the object files into the second executable
$(EXECUTABLE_2): $(OBJECT_FILES_2)
	$(COMPILER) $(COMPILER_FLAGS) -o $(EXECUTABLE_2) $(OBJECT_FILES_2)
	rm -f $(OBJECT_FILES_2)  # Remove object files after creating the executable

# Pattern rule to compile source files into object files
# $< is the first prerequisite (source file), $@ is the target (object file)
%.o: %.cpp
	$(COMPILER) $(COMPILER_FLAGS) -c $< -o $@

# Rule to clean up generated files
clean:
	rm -f $(EXECUTABLE_1) $(EXECUTABLE_2)

# Declare phony targets to avoid conflicts with files of the same name
.PHONY: all clean

