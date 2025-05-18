build:
	javac -d . -cp .  regexredux.java
	native-image --silent --gc=G1 -cp . -O3 -march=native regexredux -o regexredux.run

run:
	./regexredux.run 0 < ../../input/regexredux.input
