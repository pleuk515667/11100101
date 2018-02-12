#include "cryptotools.h"
#include <fstream>
#include <algorithm>
#include <iostream>
#include <string.h>

using namespace std;

int main()
{
	CryptoTools ct;
	unsigned char iv[16] = {0};
	unsigned char *plaintext = (unsigned char *)"This is a top secret.";
	unsigned char cipherText[64];
	unsigned char *goal= (unsigned char*)"8D20E5056A8D24D0462CE74E4904C1B513E10D1DF4A2EF2AD4540FAE1CA0AAF9";
	int cipherText_len;
	
	cout << "The plaintext is: " << plaintext << endl;
	cout << "The ciphertext is: " << goal << endl;
	cout << "The IV is all zeros" << endl;
	cout << "Searching words.txt for the correct key..."  << endl;

	ifstream fin;	
	fin.open("words.txt");
	if(fin.fail())
	{
		fin.close();
		cout << "Error: words.txt not found." << endl;
		return 0;
	}
	
	string word;
	while(getline(fin,word))
	{
		while(word.length() < 16)
		{
			word.append(" ");	
		}
		cipherText_len = ct.encrypt(EVP_aes_128_cbc(), plaintext, strlen((char *)plaintext), (unsigned char*)word.c_str(), iv, cipherText);
		if(strcmp((char*)ct.strToHex(cipherText,cipherText_len),(char*)goal)==0)
		{
			word.erase(remove(word.begin(), word.end(), ' '), word.end());
			cout << "Success! The key found was: " << word << endl;
			cout << "It was used to encrypt the plaintext into: " << ct.strToHex(cipherText,cipherText_len) << endl;
			fin.close();
			return 1;
		}
	}
	cout << "Error: No Valid key found from words.txt" << endl;
	fin.close();
	return 0;
}
