build:
	javac -d . -cp .  binarytrees.java
	native-image --silent  -cp . -O3 -march=native binarytrees -o binarytrees.run

run:
	./binarytrees.run 21
