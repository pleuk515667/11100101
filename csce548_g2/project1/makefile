INC=/usr/local/ssl/include/
LIB=/usr/local/ssl/lib/

all: bfminer clean

bfminer: cryptotools.o bfkeyminer.o
	g++ -o bfminer cryptotools.o bfkeyminer.o -lcrypto -ldl

cryptotools.o: cryptotools.cpp
	g++ -c cryptotools.cpp

bfkeyminer.o: bfkeyminer.cpp
	g++ -c bfkeyminer.cpp

clean:
	rm *o
