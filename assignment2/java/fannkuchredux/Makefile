build:
	javac -d . -cp .  fannkuchredux.java
	native-image --silent --gc=G1 -cp . -O3 -march=native fannkuchredux -o fannkuchredux.out

run:
	./fannkuchredux.out 12
