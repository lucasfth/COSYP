build:
	javac -d . -cp .  nbody.java
	native-image --silent --gc=G1 -cp . -O3 -march=native nbody -o nbody.out

run:
	./nbody.out 50000000
