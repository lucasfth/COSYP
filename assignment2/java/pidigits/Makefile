build:
	javac -d . -cp .  pidigits.java
	native-image --silent --gc=G1 -cp . -O3 -march=native pidigits -o pidigits.out

run:
	./pidigits.out 10000
