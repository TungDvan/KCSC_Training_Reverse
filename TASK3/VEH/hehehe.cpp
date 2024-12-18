#include <windows.h>
#include <wincrypt.h>
#include <iostream>
#include <cstring> 

int main(){
	unsigned char flag_en[32] = 
	{
		0xE5, 0x60, 0x44, 0x09, 0x42, 0xC4, 0xBB, 0xDE, 0xF6, 0xA1, 
		0x2D, 0x93, 0xD9, 0x1D, 0x13, 0x72, 0xAF, 0x8D, 0x4C, 0xF7, 
		0xA7, 0x9F, 0x1F, 0xB9, 0x99, 0x68, 0x9C, 0xB8, 0xC2, 0x4C, 
		0x4F, 0x85
	};
	HCRYPTPROV phProv;
//	HCRYPTHASH phHash;
//	char link_Ytb[100] = "https://www.youtube.com/watch?v=dQw4w9WgXcQ";
	DWORD pdwDataLen;
	unsigned char _32_byte[32];
	if (CryptAcquireContextW(&phProv, 0, 0, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)){
		if (CryptCreateHash(phProv, CALG_SHA_256, 0, 0, &phHash)){
			if (CryptHashData(phHash, (BYTE*)link_Ytb, strlen(link_Ytb), 0)){
				pdwDataLen = 32;
                CryptGetHashParam(phHash, HP_HASHVAL, (BYTE*)_32_byte, &pdwDataLen, 0);
                CryptDestroyHash(phHash);
                CryptReleaseContext(phProv, 0);
			}
		}		
	}

	
	unsigned char pbData[50] =
	{
		0x08, 0x02, 0x00, 0x00, 0x10, 0x66, 0x00, 0x00, 0x20, 0x00, 
		0x00, 0x00, 0x04, 0x24, 0x97, 0x4C, 0x68, 0x53, 0x02, 0x90, 
		0x45, 0x8C, 0x8D, 0x58, 0x67, 0x4E, 0x26, 0x37, 0xF6, 0x5A, 
		0xBC, 0x12, 0x70, 0x57, 0x95, 0x7D, 0x7B, 0x3A, 0xCB, 0xD2, 
		0x4C, 0x20, 0x8F, 0x93
	};
//	unsigned char flag[32] =
//	{
//		0x74, 0x75, 0x6E, 0x67, 0x64, 0x76, 0x61, 0x6E, 0x64, 0x65, 
//		0x70, 0x74, 0x72, 0x61, 0x69, 0x74, 0x68, 0x69, 0x63, 0x68, 
//		0x62, 0x61, 0x63, 0x68, 0x68, 0x61, 0x69, 0x70, 0x68, 0x75, 
//		0x6F, 0x6E
//	};
	
	HCRYPTKEY phKey;
	int v6[4] = 
	{
		0x01, 0x00, 0x00, 0x00
	};
	unsigned char pbIV[16] = 
	{
		0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A, 
		0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10
	};
	if (CryptAcquireContextW(&phProv, 0, L"Microsoft Enhanced RSA and AES Cryptographic Provider", PROV_RSA_AES, CRYPT_VERIFYCONTEXT)){
		if (CryptImportKey(phProv, (BYTE*)pbData, 0x2Cu, 0, 0, &phKey)){
			if (CryptSetKeyParam(phKey, KP_MODE, (BYTE*)v6, 0) && CryptSetKeyParam(phKey, KP_IV, (BYTE*)pbIV, 0)){
				DWORD pdwDataLen = 32;		
//				if (CryptEncrypt(phKey, 0, 1, 0, (BYTE*)flag, &pdwDataLen, 0x400)){
//					for (int i = 0; i < 32; i++) printf("0x%x, ", flag[i]);
//				}
				if (CryptDecrypt(phKey, 0, 1, 0, (BYTE*)flag_en, &pdwDataLen)){
					for (int i = 0; i < 32; i++) printf("%c", flag_en[i]);
				}
			}
		}
	}
}

