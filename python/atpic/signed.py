#!/usr/bin/python3
import ctypes
# http://en.wikipedia.org/wiki/Integer_%28computer_science%29
# http://en.wikipedia.org/wiki/Signed_number_representations
# http://stackoverflow.com/questions/1375897/how-to-get-the-signed-integer-value-of-a-long-in-python
# ctypes 
# c_byte 	char 	int/long
# c_ubyte 	unsigned char 	int/long
# c_short 	short 	int/long
# c_ushort 	unsigned short 	int/long
# c_int 	int 	int/long
# c_uint 	unsigned int 	int/long
# c_long 	long 	int/long
# c_ulong 	unsigned long 	int/long

def signed2unsigned(nb,bits):
    if bits <=8:
        fct=ctypes.c_ubyte
    elif bits <=16:
        fct=ctypes.c_ushort
    elif bits <=32:
        fct=ctypes.c_uint
    elif bits <=64:
        fct=ctypes.c_ulong

    newnb=fct(nb).value
    return newnb

# ctypes.c_byte(unsigned).value

def unsigned2signed(nb,bits):
    if bits <=8:
        fct=ctypes.c_byte
    elif bits <=16:
        fct=ctypes.c_short
    elif bits <=32:
        fct=ctypes.c_int
    elif bits <=64:
        fct=ctypes.c_long

    newnb=fct(nb).value
    return newnb

if __name__ == "__main__":
    wlen=8
    for unsigned in  range(0,1<<wlen):
        # signed_number = ctypes.c_byte(unsigned).value
        signed_number=unsigned2signed(unsigned,wlen)
        unsigned2=signed2unsigned(signed_number,wlen)
        print(unsigned,unsigned2,signed_number,bin(unsigned),bin(signed_number))
