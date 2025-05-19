build:
	javac -d . -cp .  reversecomplement.java
	native-image --silent --gc=G1 -cp . -O3 -march=native reversecomplement -o reversecomplement.out

run:
	./reversecomplement.out 0 < ../../input/revcomp-input100000001.txt
