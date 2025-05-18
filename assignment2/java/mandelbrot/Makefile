build:
	javac -d . -cp .  mandelbrot.java
	native-image --silent --gc=G1 -cp . -O3 -march=native mandelbrot -o mandelbrot.run

run:
	./mandelbrot.run 16000
