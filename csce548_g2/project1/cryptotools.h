#ifndef cryptotools_h
#define cryptotools_h
#include <openssl/evp.h>
#include <openssl/err.h>
#include <openssl/conf.h>

class CryptoTools
{
public:
	int encrypt(const EVP_CIPHER*, unsigned char*, int, unsigned char*, unsigned char*, unsigned char*);
	int decrypt(const EVP_CIPHER*, unsigned char*, int, unsigned char*, unsigned char*, unsigned char*);
	char* strToHex(unsigned char*, int);
private:
	void handleErrors();
};
#endif
