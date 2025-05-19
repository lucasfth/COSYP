build:
	javac -d . -cp .  regexredux.java
	native-image --silent --gc=G1 -cp . -O3 -march=native regexredux -o regexredux.out

run:
	./regexredux.out 0 < ../../input/regexredux-input5000000.txt

