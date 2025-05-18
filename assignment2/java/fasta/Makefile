build:
	javac -d . -cp . fasta.java
	native-image --silent --gc=G1 -cp . -O3 -march=native fasta -o fasta.run

run:
	./fasta.run 25000000
