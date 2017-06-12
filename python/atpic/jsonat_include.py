#!/usr/bin/python3
# ctyps wrapper to libyajl
# inspired by:
# http://pykler.github.com/yajl-py/
# libyajl2 - Yet Another JSON Library

# why?
# =========
# because i do not want to decode encode /decode encode
# because It could convert directly to XML

from ctypes import *
from ctypes.util import find_library

YAJL_LIBRARY = find_library('yajl')
if not YAJL_LIBRARY:
    raise OSError('Cannot find libyajl in the system')
# libya
yajl = cdll.LoadLibrary(YAJL_LIBRARY)

# print(libya)

# some functions:

yajl.yajl_alloc.restype =  c_void_p # c_char_p # POINTER(c_char)  # c_void_p
yajl.yajl_alloc.argtypes = [c_void_p, c_void_p, c_void_p]

yajl.yajl_config.restype = c_int

yajl.yajl_free.argtypes = [c_void_p]

yajl.yajl_parse.restype = c_int

yajl.yajl_parse.argtypes = [c_void_p, c_char_p, c_size_t]

yajl.yajl_complete_parse.restype = c_int
yajl.yajl_complete_parse.argtypes = [c_void_p]

yajl.yajl_get_error.restype = c_char_p
yajl.yajl_get_error.argtypes = [c_void_p, c_int, c_char_p, c_size_t]

yajl.yajl_get_bytes_consumed.restype = c_uint
yajl.yajl_get_bytes_consumed.argtypes = [c_void_p, c_char_p]


# Callback Functions
YAJL_NULL = CFUNCTYPE(c_int, c_void_p)
YAJL_BOOL = CFUNCTYPE(c_int, c_void_p, c_int)
YAJL_INT  = CFUNCTYPE(c_int, c_void_p, c_longlong)
YAJL_DBL  = CFUNCTYPE(c_int, c_void_p, c_double)
YAJL_NUM  = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_STR  = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_SDCT = CFUNCTYPE(c_int, c_void_p)
YAJL_DCTK = CFUNCTYPE(c_int, c_void_p, POINTER(c_ubyte), c_uint)
YAJL_EDCT = CFUNCTYPE(c_int, c_void_p)
YAJL_SARR = CFUNCTYPE(c_int, c_void_p)
YAJL_EARR = CFUNCTYPE(c_int, c_void_p)
class yajl_callbacks(Structure):
    _fields_ = [
        ("yajl_null",           YAJL_NULL),
        ("yajl_boolean",        YAJL_BOOL),
        ("yajl_integer",        YAJL_INT ),
        ("yajl_double",         YAJL_DBL ),
        ("yajl_number",         YAJL_NUM ),
        ("yajl_string",         YAJL_STR ),
        ("yajl_start_map",      YAJL_SDCT),
        ("yajl_map_key",        YAJL_DCTK),
        ("yajl_end_map",        YAJL_EDCT),
        ("yajl_start_array",    YAJL_SARR),
        ("yajl_end_array",      YAJL_EARR),
    ]

# yajl option
(
yajl_allow_comments,
yajl_dont_validate_strings,
yajl_allow_trailing_garbage,
yajl_allow_multiple_values,
yajl_allow_partial_values
) = map(c_int, [2**x for x in range(5)])

# yajl_status
(
yajl_status_ok,
yajl_status_client_canceled,
yajl_status_error
) = map(c_int, range(3))


if __name__ == "__main__":
    print("testing json")
    
