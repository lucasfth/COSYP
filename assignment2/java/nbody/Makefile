build:
	javac -d . -cp .  nbody.java
	native-image --silent --gc=G1 -cp . -O3 -march=native nbody -o nbody.run

run:
	./nbody.run 50000000
