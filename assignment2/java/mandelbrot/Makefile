build:
	javac -d . -cp .  mandelbrot.java
	native-image --silent --gc=G1 -cp . -O3 -march=native mandelbrot -o mandelbrot.out

run:
	./mandelbrot.out 16000
