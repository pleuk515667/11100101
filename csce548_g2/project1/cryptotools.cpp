#include "cryptotools.h"

/**
    Takes a string as an arguement and returns it's hexadecimal representation.

    @param str The input string to be converted.
    @param len The length of the input string.	
    @return The hexadecimal representation of the input string.
*/
char* CryptoTools::strToHex(unsigned char* str, int len)
{
	char* buffer = new char[len*2+1];
	char* pbuffer = buffer;
	for(int i = 0; i < len ; ++i )
	{
		sprintf(pbuffer, "%02X", str[i]);
		pbuffer += 2;
	}
	return buffer;
}

/**
    Encrypts a plaintext with a given crypto mode and insersts the ciphertext into a string.
    
    @param mode The crypto mode used to encrypt the plaintext. Ex: EVP_aes_128_cbc().
    @param plaintext The plaintext to be encrypted.
    @param plaintext_len The length of the plaintext.
    @param key The key used to encrypt the plaintext.
    @param iv The initialization vector used to encrypt the plaintext.
    @param ciphertext The string used to store the encrypted plaintext.
    @return The length of the ciphertext.
*/
int CryptoTools::encrypt(const EVP_CIPHER* mode, unsigned char *plaintext, int plaintext_len, unsigned char *key, unsigned char *iv, unsigned char *ciphertext)
{
	EVP_CIPHER_CTX *ctx;

	int len;
	
	int ciphertext_len;

	if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

	if(1 != EVP_EncryptInit_ex(ctx, mode, NULL, key, iv)) handleErrors();

	EVP_CIPHER_CTX_set_padding(ctx,1);

	if(1 != EVP_EncryptUpdate(ctx, ciphertext, &len, plaintext, plaintext_len)) handleErrors();

	ciphertext_len = len;

	if(1 != EVP_EncryptFinal_ex(ctx, ciphertext + len, &len)) handleErrors();

	ciphertext_len += len;

	EVP_CIPHER_CTX_free(ctx);

	return ciphertext_len;
}

/**
    Decrypts a ciphertext with a given crypto mode and inserts the the plaintext into a string.

    @param mode The crypto mode used to encrypt the plaintext. Ex: EVP_aes_128_cbc().
    @param ciphertext The ciphertext to be decrypted.
    @param ciphertext_len The length of the ciphertext.
    @param key The key used to decrypt the ciphertext.
    @param iv The initialization vector used to decrypt the plaintext.
    @param plaintext The string used to store the decrypted ciphertext.
    @return The length of the plaintext.
*/
int CryptoTools::decrypt(const EVP_CIPHER* mode, unsigned char *ciphertext, int ciphertext_len, unsigned char *key, unsigned char *iv, unsigned char *plaintext)
{
	EVP_CIPHER_CTX *ctx;

	int len;

	int plaintext_len;

	if(!(ctx = EVP_CIPHER_CTX_new())) handleErrors();

	if(1 != EVP_DecryptInit_ex(ctx, EVP_aes_128_cbc(), NULL, key, iv)) handleErrors();

	EVP_CIPHER_CTX_set_padding(ctx,1);

	if(1 != EVP_DecryptUpdate(ctx, plaintext, &len, ciphertext, ciphertext_len)) handleErrors();
	plaintext_len = len;

	if(1 != EVP_DecryptFinal_ex(ctx, plaintext + len, &len)) handleErrors();
	plaintext_len += len;
  
	EVP_CIPHER_CTX_free(ctx);

	return plaintext_len;
}

/**
    Handles any errors thrown during the encryption/decryption process.
*/
void CryptoTools::handleErrors()
{
	ERR_print_errors_fp(stderr);
	abort();
}
