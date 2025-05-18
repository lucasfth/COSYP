build:
	javac -d . -cp .  spectralnorm.java
	native-image --silent --gc=G1 -cp . -O3 -march=native spectralnorm -o spectralnorm.run

run:
	./reversecomplement.run 5500
