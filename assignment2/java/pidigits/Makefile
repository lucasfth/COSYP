build:
	javac -d . -cp .  pidigits.java
	native-image --silent --gc=G1 -cp . -O3 -march=native pidigits -o pidigits.run

run:
	./pidigits.run 10000
