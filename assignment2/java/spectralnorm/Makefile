build:
	javac -d . -cp .  spectralnorm.java
	native-image --silent --gc=G1 -cp . -O3 -march=native spectralnorm -o spectralnorm.out

run:
	./spectralnorm.out 5500
