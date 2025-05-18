build:
	javac -d . -cp .  reversecomplement.java
	native-image --silent --gc=G1 -cp . -O3 -march=native reversecomplement -o reversecomplement.run

run:
	./reversecomplement.run 0 < ../../input/reversecomplement.input
