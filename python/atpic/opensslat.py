#!/usr/bin/python3
#  a ctypes wrapper of openssl
# dpkg -L libssl1.0.0
# /usr/lib/x86_64-linux-gnu/libcrypto.so.1.0.0
# /usr/lib/x86_64-linux-gnu/libssl.so.1.0.0
# inspired by http://code.google.com/p/ctypescrypto/source/checkout
# Note: this is different from: dpkg -L python3-openssl

# python-ctypeslib - code generator to convert header files into ctypes interfaces
# libssl-dev
# /usr/include/openssl/crypto.h
# /usr/include/openssl/evp.h
# h2xml /usr/include/openssl/evp.h
# xml2py  -I  /usr/include/openssl evp.xml -o evp.py
# xml2py -l crypto evp.xml -o evp.py
# *** the -l option is very important

# or: python3-crypto 
# more /usr/lib/python3/dist-packages/Crypto/Cipher/Blowfish.py

import traceback
from ctypes import *
from ctypes.util import find_library

import atpic.log
xx=atpic.log.setmod("INFO","opensslat")

CRYPTO_LIBRARY = find_library('crypto')
if not CRYPTO_LIBRARY:
    raise OSError('Cannot find libcrypto in the system')
# libya
libcrypto = cdll.LoadLibrary(CRYPTO_LIBRARY)



STRING = c_char_p
WSTRING = c_wchar_p

class evp_cipher_st(Structure):
    pass
EVP_CIPHER = evp_cipher_st

class evp_cipher_ctx_st(Structure):
    pass
EVP_CIPHER_CTX = evp_cipher_ctx_st

class engine_st(Structure):
    pass
ENGINE = engine_st


libcrypto.OpenSSL_add_all_digests.restype = None
libcrypto.OpenSSL_add_all_digests.argtypes = []

libcrypto.OpenSSL_add_all_ciphers.restype = None
libcrypto.OpenSSL_add_all_ciphers.argtypes = []


libcrypto.EVP_get_cipherbyname.restype = POINTER(EVP_CIPHER)
libcrypto.EVP_get_cipherbyname.argtypes = [STRING]

libcrypto.EVP_get_cipherbyname.restype = POINTER(EVP_CIPHER)
libcrypto.EVP_get_cipherbyname.argtypes = [STRING]


libcrypto.EVP_CIPHER_CTX_new.restype = POINTER(EVP_CIPHER_CTX)
libcrypto.EVP_CIPHER_CTX_new.argtypes = []

libcrypto.EVP_CipherInit_ex.restype = c_int
libcrypto.EVP_CipherInit_ex.argtypes = [POINTER(EVP_CIPHER_CTX), POINTER(EVP_CIPHER), POINTER(ENGINE), POINTER(c_ubyte), POINTER(c_ubyte), c_int]



libcrypto.EVP_CipherUpdate.restype = c_int
libcrypto.EVP_CipherUpdate.argtypes = [POINTER(EVP_CIPHER_CTX), POINTER(c_ubyte), POINTER(c_int), POINTER(c_ubyte), c_int]

libcrypto.EVP_CipherFinal.restype = c_int
libcrypto.EVP_CipherFinal.argtypes = [POINTER(EVP_CIPHER_CTX), POINTER(c_ubyte), POINTER(c_int)]

libcrypto.EVP_CipherFinal_ex.restype = c_int
libcrypto.EVP_CipherFinal_ex.argtypes = [POINTER(EVP_CIPHER_CTX), POINTER(c_ubyte), POINTER(c_int)]



class env_md_st(Structure):
    pass
EVP_MD = env_md_st



libcrypto.EVP_BytesToKey.restype = c_int
libcrypto.EVP_BytesToKey.argtypes = [POINTER(EVP_CIPHER), POINTER(EVP_MD), POINTER(c_ubyte), POINTER(c_ubyte), c_int, c_int, POINTER(c_ubyte), POINTER(c_ubyte)]

libcrypto.EVP_md5.restype = POINTER(EVP_MD)
libcrypto.EVP_md5.argtypes = []

class ErrorCrypto(Exception):
    pass
	
def list2ubytes(data):
    yy=atpic.log.setname(xx,'list2ubytes')
    data_p=(c_ubyte * (len(data)))() # last byte is zero
    for i in range(0,len(data)):
        data_p[i]=data[i]
    return data_p


def bytes2ubytes(data):
    yy=atpic.log.setname(xx,'bytes2ubytes')
    data_p=(c_ubyte * (len(data)))() # last byte is zero
    for i in range(0,len(data)):
        data_p[i]=data[i]
    return data_p

def myclean_ctx(ctx):
    yy=atpic.log.setname(xx,'myclean_ctx')
    libcrypto.EVP_CIPHER_CTX_cleanup(ctx)
    libcrypto.EVP_CIPHER_CTX_free(ctx)
    libcrypto.EVP_cleanup()
    libcrypto.CRYPTO_cleanup_all_ex_data() # necessary?

def encrypt(data,passphrase,ciphername=b'BF-CBC',enc=1):
    """
    INPUT:
    data: bytes to encode
    passphrase: bytes
    cyphername: one of ./crypto/objects/obj_mac.h
    e.g: 'AES-256-CBC','BF-CBC'
    enc: 1 if need to encode, 0 if need to decode
    OUTPUT:
    encoded bytes.
    """
    yy=atpic.log.setname(xx,'encrypt')
    atpic.log.debug(yy,'input',data,passphrase,ciphername,enc)
    libcrypto.OpenSSL_add_all_digests()
    libcrypto.OpenSSL_add_all_ciphers()

    data_p=bytes2ubytes(data)
    passphrase_p=bytes2ubytes(passphrase)

    # ciphername=b'AES-256-CBC'
    cipher=libcrypto.EVP_get_cipherbyname(ciphername)
    # man EVP_get_cipherbyname
    # iv = IV = http://en.wikipedia.org/wiki/Initialization_vector

    # openssl enc -aes-128-cbc -k secret -P -md sha1
    # salt=03AA05126BBCF372
    # key=1B1D867E5B65A515047A3DE87F9F6410
    # iv =F5394D35B2BA5795AFFA47733652852F
    """
    So in openssl Key & IV are computed by calling this function (source
    lines: 552-554 from apps/enc.c ):
    
    EVP_BytesToKey(cipher,dgst,sptr,
    (unsigned char *)str,
    strlen(str),1,key,iv)
    
    where str is the passphrase 
    """


    sptr=None # NULL salt
    EVP_MAX_KEY_LENGTH=64 # ./crypto/evp/evp.h:#define EVP_MAX_KEY_LENGTH 
    EVP_MAX_IV_LENGTH=16  # ./crypto/evp/evp.h:#define EVP_MAX_IV_LENGTH
    key=(c_ubyte*EVP_MAX_KEY_LENGTH)()
    iv=(c_ubyte*EVP_MAX_IV_LENGTH)()
    dgst = libcrypto.EVP_md5()
    atpic.log.debug(yy,'len(passphrase_p)',len(passphrase_p))
    keysize=libcrypto.EVP_BytesToKey(cipher,dgst,sptr,passphrase_p,len(passphrase_p),1,key,iv)
    atpic.log.debug(yy,'key',key[:])
    atpic.log.debug(yy,'iv',iv[:])
    atpic.log.debug(yy,'keysize',keysize)
    ctx = libcrypto.EVP_CIPHER_CTX_new(cipher, None, key, iv)
    if ctx == 0:
        raise ErrorCrypto("Unable to create cipher context")
    # http://stackoverflow.com/questions/12013599/how-to-cast-multiple-integers-as-a-ctypes-array-of-c-ubyte-in-python
    # ctypes.ArgumentError: argument 4: <class 'TypeError'>: expected LP_c_ubyte instance instead of bytes
    
    result = libcrypto.EVP_CipherInit_ex(ctx, cipher, None, key, iv, enc)
    if result == 0:
        myclean_ctx(ctx)
        raise ErrorCrypto("Unable to initialize cipher")
        

    cipher_out_len=c_int(0)
    cipher_out = (c_ubyte * (len(data_p) + 32))()
    
    # http://bb10.com/python-comtypes-user/2012-01/msg00001.html
    # result=libcrypto.EVP_CipherUpdate(ctx, cipher_out, byref(cipher_out_len), c_char_p(data), len(data))
    # http://stackoverflow.com/questions/9537460/python-ctype-help-working-with-c-unsigned-char-pointers
    result=libcrypto.EVP_CipherUpdate(ctx, cipher_out, byref(cipher_out_len), data_p, len(data_p))
    if result == 0:
        myclean_ctx(ctx)
        raise ErrorCrypto("Unable to update cipher")
    atpic.log.debug(yy,'cipher_out_len',cipher_out_len.value)
    #
    
    update_data = cipher_out[:cipher_out_len.value]
    result = libcrypto.EVP_CipherFinal_ex(ctx, cipher_out, byref(cipher_out_len))
    if result == 0:
        myclean_ctx(ctx)
        raise ErrorCrypto("Unable to finalize cipher")

    final_data = cipher_out[:cipher_out_len.value]
    atpic.log.debug(yy,'cipher_out_len final',cipher_out_len.value)
    whole_data=update_data + final_data
    whole_data_bytes=bytes(whole_data)
    # A typical application will call OpenSSL_add_all_algorithms() initially and EVP_cleanup() before exiting.
    myclean_ctx(ctx)
    atpic.log.debug(yy,'will return',whole_data_bytes)
    return whole_data_bytes


if __name__ == "__main__":
    print("hi")
    data=b'some text to encrypt2 more more more moe more more'
    key=b'some super long keeyyyyvsdsdffifdifsdisfdisfdisdisfdfisdfsdfisdsfids0123456789'
    
    out=encrypt(data,key)
    print(out)
    out2=encrypt(out,key,enc=0)
    
    print('out',out)
    print('out2',out2)
    print('data',data)

