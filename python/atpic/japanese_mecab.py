#!/usr/bin/python3
# WARNING you need the UTF8 mecab!!!!!
# apt-get install mecab-jumandic-utf8 mecab-ipadic-utf8 libmecab2 mecab-utils

'''Wrapper for mecab.h

Generated with:
./ctypesgen.py -lmecab /usr/include/mecab.h -o mecab.py

Do not modify this file.
'''

__docformat__ =  'restructuredtext'

# Begin preamble

import ctypes, os, sys
from ctypes import *

_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types

class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]

def POINTER(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p

class UserString:
    def __init__(self, seq):
        if isinstance(seq, str):
            self.data = seq
        elif isinstance(seq, UserString):
            self.data = seq.data[:]
        else:
            self.data = str(seq)
    def __str__(self): return str(self.data)
    def __repr__(self): return repr(self.data)
    def __int__(self): return int(self.data)
    def __long__(self): return int(self.data)
    def __float__(self): return float(self.data)
    def __complex__(self): return complex(self.data)
    def __hash__(self): return hash(self.data)

    def __cmp__(self, string):
        if isinstance(string, UserString):
            return cmp(self.data, string.data)
        else:
            return cmp(self.data, string)
    def __contains__(self, char):
        return char in self.data

    def __len__(self): return len(self.data)
    def __getitem__(self, index): return self.__class__(self.data[index])
    def __getslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        return self.__class__(self.data[start:end])

    def __add__(self, other):
        if isinstance(other, UserString):
            return self.__class__(self.data + other.data)
        elif isinstance(other, str):
            return self.__class__(self.data + other)
        else:
            return self.__class__(self.data + str(other))
    def __radd__(self, other):
        if isinstance(other, str):
            return self.__class__(other + self.data)
        else:
            return self.__class__(str(other) + self.data)
    def __mul__(self, n):
        return self.__class__(self.data*n)
    __rmul__ = __mul__
    def __mod__(self, args):
        return self.__class__(self.data % args)

    # the following methods are defined in alphabetical order:
    def capitalize(self): return self.__class__(self.data.capitalize())
    def center(self, width, *args):
        return self.__class__(self.data.center(width, *args))
    def count(self, sub, start=0, end=sys.maxsize):
        return self.data.count(sub, start, end)
    def decode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.decode(encoding, errors))
            else:
                return self.__class__(self.data.decode(encoding))
        else:
            return self.__class__(self.data.decode())
    def encode(self, encoding=None, errors=None): # XXX improve this?
        if encoding:
            if errors:
                return self.__class__(self.data.encode(encoding, errors))
            else:
                return self.__class__(self.data.encode(encoding))
        else:
            return self.__class__(self.data.encode())
    def endswith(self, suffix, start=0, end=sys.maxsize):
        return self.data.endswith(suffix, start, end)
    def expandtabs(self, tabsize=8):
        return self.__class__(self.data.expandtabs(tabsize))
    def find(self, sub, start=0, end=sys.maxsize):
        return self.data.find(sub, start, end)
    def index(self, sub, start=0, end=sys.maxsize):
        return self.data.index(sub, start, end)
    def isalpha(self): return self.data.isalpha()
    def isalnum(self): return self.data.isalnum()
    def isdecimal(self): return self.data.isdecimal()
    def isdigit(self): return self.data.isdigit()
    def islower(self): return self.data.islower()
    def isnumeric(self): return self.data.isnumeric()
    def isspace(self): return self.data.isspace()
    def istitle(self): return self.data.istitle()
    def isupper(self): return self.data.isupper()
    def join(self, seq): return self.data.join(seq)
    def ljust(self, width, *args):
        return self.__class__(self.data.ljust(width, *args))
    def lower(self): return self.__class__(self.data.lower())
    def lstrip(self, chars=None): return self.__class__(self.data.lstrip(chars))
    def partition(self, sep):
        return self.data.partition(sep)
    def replace(self, old, new, maxsplit=-1):
        return self.__class__(self.data.replace(old, new, maxsplit))
    def rfind(self, sub, start=0, end=sys.maxsize):
        return self.data.rfind(sub, start, end)
    def rindex(self, sub, start=0, end=sys.maxsize):
        return self.data.rindex(sub, start, end)
    def rjust(self, width, *args):
        return self.__class__(self.data.rjust(width, *args))
    def rpartition(self, sep):
        return self.data.rpartition(sep)
    def rstrip(self, chars=None): return self.__class__(self.data.rstrip(chars))
    def split(self, sep=None, maxsplit=-1):
        return self.data.split(sep, maxsplit)
    def rsplit(self, sep=None, maxsplit=-1):
        return self.data.rsplit(sep, maxsplit)
    def splitlines(self, keepends=0): return self.data.splitlines(keepends)
    def startswith(self, prefix, start=0, end=sys.maxsize):
        return self.data.startswith(prefix, start, end)
    def strip(self, chars=None): return self.__class__(self.data.strip(chars))
    def swapcase(self): return self.__class__(self.data.swapcase())
    def title(self): return self.__class__(self.data.title())
    def translate(self, *args):
        return self.__class__(self.data.translate(*args))
    def upper(self): return self.__class__(self.data.upper())
    def zfill(self, width): return self.__class__(self.data.zfill(width))

class MutableString(UserString):
    """mutable string objects

    Python strings are immutable objects.  This has the advantage, that
    strings may be used as dictionary keys.  If this property isn't needed
    and you insist on changing string values in place instead, you may cheat
    and use MutableString.

    But the purpose of this class is an educational one: to prevent
    people from inventing their own mutable string class derived
    from UserString and than forget thereby to remove (override) the
    __hash__ method inherited from UserString.  This would lead to
    errors that would be very hard to track down.

    A faster and better solution is to rewrite your program using lists."""
    def __init__(self, string=""):
        self.data = string
    def __hash__(self):
        raise TypeError("unhashable type (it is mutable)")
    def __setitem__(self, index, sub):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + sub + self.data[index+1:]
    def __delitem__(self, index):
        if index < 0:
            index += len(self.data)
        if index < 0 or index >= len(self.data): raise IndexError
        self.data = self.data[:index] + self.data[index+1:]
    def __setslice__(self, start, end, sub):
        start = max(start, 0); end = max(end, 0)
        if isinstance(sub, UserString):
            self.data = self.data[:start]+sub.data+self.data[end:]
        elif isinstance(sub, str):
            self.data = self.data[:start]+sub+self.data[end:]
        else:
            self.data =  self.data[:start]+str(sub)+self.data[end:]
    def __delslice__(self, start, end):
        start = max(start, 0); end = max(end, 0)
        self.data = self.data[:start] + self.data[end:]
    def immutable(self):
        return UserString(self.data)
    def __iadd__(self, other):
        if isinstance(other, UserString):
            self.data += other.data
        elif isinstance(other, str):
            self.data += other
        else:
            self.data += str(other)
        return self
    def __imul__(self, n):
        self.data *= n
        return self

class String(MutableString, Union):

    _fields_ = [('raw', POINTER(c_char)),
                ('data', c_char_p)]

    def __init__(self, obj=""):
        if isinstance(obj, (str, UserString)):
            self.data = str(obj)
        else:
            self.raw = obj

    def __len__(self):
        return self.data and len(self.data) or 0

    def from_param(cls, obj):
        # Convert None or 0
        if obj is None or obj == 0:
            return cls(POINTER(c_char)())

        # Convert from String
        elif isinstance(obj, String):
            return obj

        # Convert from str
        elif isinstance(obj, str):
            return cls(obj)

        # Convert from c_char_p
        elif isinstance(obj, c_char_p):
            return obj

        # Convert from POINTER(c_char)
        elif isinstance(obj, POINTER(c_char)):
            return obj

        # Convert from raw pointer
        elif isinstance(obj, int):
            return cls(cast(obj, POINTER(c_char)))

        # Convert from object
        else:
            # return String.from_param(obj._as_parameter_) # ALEX
            return String

    from_param = classmethod(from_param)

def ReturnString(obj, func=None, arguments=None):
    return String.from_param(obj)

# As of ctypes 1.0, ctypes does not support custom error-checking
# functions on callbacks, nor does it support custom datatypes on
# callbacks, so we must ensure that all callbacks return
# primitive datatypes.
#
# Non-primitive return values wrapped with UNCHECKED won't be
# typechecked, and will be converted to c_void_p.
def UNCHECKED(type):
    if (hasattr(type, "_type_") and isinstance(type._type_, str)
        and type._type_ != "P"):
        return type
    else:
        return c_void_p

# ctypes doesn't have direct support for variadic functions, so we have to write
# our own wrapper class
class _variadic_function(object):
    def __init__(self,func,restype,argtypes):
        self.func=func
        self.func.restype=restype
        self.argtypes=argtypes
    def _as_parameter_(self):
        # So we can pass this variadic function as a function pointer
        return self.func
    def __call__(self,*args):
        fixed_args=[]
        i=0
        for argtype in self.argtypes:
            # Typecheck what we can
            fixed_args.append(argtype.from_param(args[i]))
            i+=1
        return self.func(*fixed_args+list(args[i:]))

# End preamble

_libs = {}
_libdirs = []

# Begin loader

# ----------------------------------------------------------------------------
# Copyright (c) 2008 David James
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import os.path, re, sys, glob
import ctypes
import ctypes.util

def _environ_path(name):
    if name in os.environ:
        return os.environ[name].split(":")
    else:
        return []

class LibraryLoader(object):
    def __init__(self):
        self.other_dirs=[]

    def load_library(self,libname):
        """Given the name of a library, load it."""
        paths = self.getpaths(libname)

        for path in paths:
            if os.path.exists(path):
                return self.load(path)

        raise ImportError("%s not found." % libname)

    def load(self,path):
        """Given a path to a library, load it."""
        try:
            # Darwin requires dlopen to be called with mode RTLD_GLOBAL instead
            # of the default RTLD_LOCAL.  Without this, you end up with
            # libraries not being loadable, resulting in "Symbol not found"
            # errors
            if sys.platform == 'darwin':
                return ctypes.CDLL(path, ctypes.RTLD_GLOBAL)
            else:
                return ctypes.cdll.LoadLibrary(path)
        except OSError as e:
            raise ImportError(e)

    def getpaths(self,libname):
        """Return a list of paths where the library might be found."""
        if os.path.isabs(libname):
            yield libname
        else:
            # FIXME / TODO return '.' and os.path.dirname(__file__)
            for path in self.getplatformpaths(libname):
                yield path

            path = ctypes.util.find_library(libname)
            if path: yield path

    def getplatformpaths(self, libname):
        return []

# Darwin (Mac OS X)

class DarwinLibraryLoader(LibraryLoader):
    name_formats = ["lib%s.dylib", "lib%s.so", "lib%s.bundle", "%s.dylib",
                "%s.so", "%s.bundle", "%s"]

    def getplatformpaths(self,libname):
        if os.path.pathsep in libname:
            names = [libname]
        else:
            names = [format % libname for format in self.name_formats]

        for dir in self.getdirs(libname):
            for name in names:
                yield os.path.join(dir,name)

    def getdirs(self,libname):
        '''Implements the dylib search as specified in Apple documentation:

        http://developer.apple.com/documentation/DeveloperTools/Conceptual/
            DynamicLibraries/Articles/DynamicLibraryUsageGuidelines.html

        Before commencing the standard search, the method first checks
        the bundle's ``Frameworks`` directory if the application is running
        within a bundle (OS X .app).
        '''

        dyld_fallback_library_path = _environ_path("DYLD_FALLBACK_LIBRARY_PATH")
        if not dyld_fallback_library_path:
            dyld_fallback_library_path = [os.path.expanduser('~/lib'),
                                          '/usr/local/lib', '/usr/lib']

        dirs = []

        if '/' in libname:
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))
        else:
            dirs.extend(_environ_path("LD_LIBRARY_PATH"))
            dirs.extend(_environ_path("DYLD_LIBRARY_PATH"))

        dirs.extend(self.other_dirs)
        dirs.append(".")
        dirs.append(os.path.dirname(__file__))

        if hasattr(sys, 'frozen') and sys.frozen == 'macosx_app':
            dirs.append(os.path.join(
                os.environ['RESOURCEPATH'],
                '..',
                'Frameworks'))

        dirs.extend(dyld_fallback_library_path)

        return dirs

# Posix

class PosixLibraryLoader(LibraryLoader):
    _ld_so_cache = None

    def _create_ld_so_cache(self):
        # Recreate search path followed by ld.so.  This is going to be
        # slow to build, and incorrect (ld.so uses ld.so.cache, which may
        # not be up-to-date).  Used only as fallback for distros without
        # /sbin/ldconfig.
        #
        # We assume the DT_RPATH and DT_RUNPATH binary sections are omitted.

        directories = []
        for name in ("LD_LIBRARY_PATH",
                     "SHLIB_PATH", # HPUX
                     "LIBPATH", # OS/2, AIX
                     "LIBRARY_PATH", # BE/OS
                    ):
            if name in os.environ:
                directories.extend(os.environ[name].split(os.pathsep))
        directories.extend(self.other_dirs)
        directories.append(".")
        directories.append(os.path.dirname(__file__))

        try: directories.extend([dir.strip() for dir in open('/etc/ld.so.conf')])
        except IOError: pass

        directories.extend(['/lib', '/usr/lib', '/lib64', '/usr/lib64'])

        cache = {}
        lib_re = re.compile(r'lib(.*)\.s[ol]')
        ext_re = re.compile(r'\.s[ol]$')
        for dir in directories:
            try:
                for path in glob.glob("%s/*.s[ol]*" % dir):
                    file = os.path.basename(path)

                    # Index by filename
                    if file not in cache:
                        cache[file] = path

                    # Index by library name
                    match = lib_re.match(file)
                    if match:
                        library = match.group(1)
                        if library not in cache:
                            cache[library] = path
            except OSError:
                pass

        self._ld_so_cache = cache

    def getplatformpaths(self, libname):
        if self._ld_so_cache is None:
            self._create_ld_so_cache()

        result = self._ld_so_cache.get(libname)
        if result: yield result

        path = ctypes.util.find_library(libname)
        if path: yield os.path.join("/lib",path)

# Windows

class _WindowsLibrary(object):
    def __init__(self, path):
        self.cdll = ctypes.cdll.LoadLibrary(path)
        self.windll = ctypes.windll.LoadLibrary(path)

    def __getattr__(self, name):
        try: return getattr(self.cdll,name)
        except AttributeError:
            try: return getattr(self.windll,name)
            except AttributeError:
                raise

class WindowsLibraryLoader(LibraryLoader):
    name_formats = ["%s.dll", "lib%s.dll", "%slib.dll"]

    def load_library(self, libname):
        try:
            result = LibraryLoader.load_library(self, libname)
        except ImportError:
            result = None
            if os.path.sep not in libname:
                for name in self.name_formats:
                    try:
                        result = getattr(ctypes.cdll, name % libname)
                        if result:
                            break
                    except WindowsError:
                        result = None
            if result is None:
                try:
                    result = getattr(ctypes.cdll, libname)
                except WindowsError:
                    result = None
            if result is None:
                raise ImportError("%s not found." % libname)
        return result

    def load(self, path):
        return _WindowsLibrary(path)

    def getplatformpaths(self, libname):
        if os.path.sep not in libname:
            for name in self.name_formats:
                dll_in_current_dir = os.path.abspath(name % libname)
                if os.path.exists(dll_in_current_dir):
                    yield dll_in_current_dir
                path = ctypes.util.find_library(name % libname)
                if path:
                    yield path

# Platform switching

# If your value of sys.platform does not appear in this dict, please contact
# the Ctypesgen maintainers.

loaderclass = {
    "darwin":   DarwinLibraryLoader,
    "cygwin":   WindowsLibraryLoader,
    "win32":    WindowsLibraryLoader
}

loader = loaderclass.get(sys.platform, PosixLibraryLoader)()

def add_library_search_dirs(other_dirs):
    loader.other_dirs = other_dirs

load_library = loader.load_library

del loaderclass

# End loader

add_library_search_dirs([])

# Begin libraries

_libs["mecab"] = load_library("mecab")

# 1 libraries
# End libraries

# No modules

# /usr/include/mecab.h: 15
class struct_mecab_dictionary_info_t(Structure):
    pass

struct_mecab_dictionary_info_t.__slots__ = [
    'filename',
    'charset',
    'size',
    'type',
    'lsize',
    'rsize',
    'version',
    'next',
]
struct_mecab_dictionary_info_t._fields_ = [
    ('filename', String),
    ('charset', String),
    ('size', c_uint),
    ('type', c_int),
    ('lsize', c_uint),
    ('rsize', c_uint),
    ('version', c_ushort),
    ('next', POINTER(struct_mecab_dictionary_info_t)),
]

# /usr/include/mecab.h: 98
class struct_mecab_node_t(Structure):
    pass

# /usr/include/mecab.h: 62
class struct_mecab_path_t(Structure):
    pass

struct_mecab_path_t.__slots__ = [
    'rnode',
    'rnext',
    'lnode',
    'lnext',
    'cost',
    'prob',
]
struct_mecab_path_t._fields_ = [
    ('rnode', POINTER(struct_mecab_node_t)),
    ('rnext', POINTER(struct_mecab_path_t)),
    ('lnode', POINTER(struct_mecab_node_t)),
    ('lnext', POINTER(struct_mecab_path_t)),
    ('cost', c_int),
    ('prob', c_float),
]

struct_mecab_node_t.__slots__ = [
    'prev',
    'next',
    'enext',
    'bnext',
    'rpath',
    'lpath',
    'surface',
    'feature',
    'id',
    'length',
    'rlength',
    'rcAttr',
    'lcAttr',
    'posid',
    'char_type',
    'stat',
    'isbest',
    'alpha',
    'beta',
    'prob',
    'wcost',
    'cost',
]
struct_mecab_node_t._fields_ = [
    ('prev', POINTER(struct_mecab_node_t)),
    ('next', POINTER(struct_mecab_node_t)),
    ('enext', POINTER(struct_mecab_node_t)),
    ('bnext', POINTER(struct_mecab_node_t)),
    ('rpath', POINTER(struct_mecab_path_t)),
    ('lpath', POINTER(struct_mecab_path_t)),
    ('surface', String),
    ('feature', String),
    ('id', c_uint),
    ('length', c_ushort),
    ('rlength', c_ushort),
    ('rcAttr', c_ushort),
    ('lcAttr', c_ushort),
    ('posid', c_ushort),
    ('char_type', c_ubyte),
    ('stat', c_ubyte),
    ('isbest', c_ubyte),
    ('alpha', c_float),
    ('beta', c_float),
    ('prob', c_float),
    ('wcost', c_short),
    ('cost', c_long),
]

enum_anon_1 = c_int # /usr/include/mecab.h: 221

MECAB_NOR_NODE = 0 # /usr/include/mecab.h: 221

MECAB_UNK_NODE = 1 # /usr/include/mecab.h: 221

MECAB_BOS_NODE = 2 # /usr/include/mecab.h: 221

MECAB_EOS_NODE = 3 # /usr/include/mecab.h: 221

MECAB_EON_NODE = 4 # /usr/include/mecab.h: 221

enum_anon_2 = c_int # /usr/include/mecab.h: 248

MECAB_SYS_DIC = 0 # /usr/include/mecab.h: 248

MECAB_USR_DIC = 1 # /usr/include/mecab.h: 248

MECAB_UNK_DIC = 2 # /usr/include/mecab.h: 248

enum_anon_3 = c_int # /usr/include/mecab.h: 268

MECAB_ONE_BEST = 1 # /usr/include/mecab.h: 268

MECAB_NBEST = 2 # /usr/include/mecab.h: 268

MECAB_PARTIAL = 4 # /usr/include/mecab.h: 268

MECAB_MARGINAL_PROB = 8 # /usr/include/mecab.h: 268

MECAB_ALTERNATIVE = 16 # /usr/include/mecab.h: 268

MECAB_ALL_MORPHS = 32 # /usr/include/mecab.h: 268

MECAB_ALLOCATE_SENTENCE = 64 # /usr/include/mecab.h: 268

# /usr/include/mecab.h: 334
class struct_mecab_t(Structure):
    pass

mecab_t = struct_mecab_t # /usr/include/mecab.h: 334

# /usr/include/mecab.h: 335
class struct_mecab_model_t(Structure):
    pass

mecab_model_t = struct_mecab_model_t # /usr/include/mecab.h: 335

# /usr/include/mecab.h: 336
class struct_mecab_lattice_t(Structure):
    pass

mecab_lattice_t = struct_mecab_lattice_t # /usr/include/mecab.h: 336

mecab_dictionary_info_t = struct_mecab_dictionary_info_t # /usr/include/mecab.h: 337

mecab_node_t = struct_mecab_node_t # /usr/include/mecab.h: 338

mecab_path_t = struct_mecab_path_t # /usr/include/mecab.h: 339

# /usr/include/mecab.h: 348
if hasattr(_libs['mecab'], 'mecab_new'):
    mecab_new = _libs['mecab'].mecab_new
    # mecab_new.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_new.argtypes = [c_int, POINTER(c_char_p)]
    mecab_new.restype = POINTER(mecab_t)
    pass
# /usr/include/mecab.h: 353
if hasattr(_libs['mecab'], 'mecab_new2'):
    mecab_new2 = _libs['mecab'].mecab_new2
    # mecab_new2.argtypes = [String]
    mecab_new2.argtypes = [c_char_p]
    mecab_new2.restype = POINTER(mecab_t)

# /usr/include/mecab.h: 358
if hasattr(_libs['mecab'], 'mecab_version'):
    mecab_version = _libs['mecab'].mecab_version
    mecab_version.argtypes = []
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_version.restype = ReturnString
    else:
        mecab_version.restype = String
        mecab_version.errcheck = ReturnString

# /usr/include/mecab.h: 363
if hasattr(_libs['mecab'], 'mecab_strerror'):
    mecab_strerror = _libs['mecab'].mecab_strerror
    mecab_strerror.argtypes = [POINTER(mecab_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_strerror.restype = ReturnString
    else:
        mecab_strerror.restype = String
        mecab_strerror.errcheck = ReturnString

# /usr/include/mecab.h: 368
if hasattr(_libs['mecab'], 'mecab_destroy'):
    mecab_destroy = _libs['mecab'].mecab_destroy
    mecab_destroy.argtypes = [POINTER(mecab_t)]
    mecab_destroy.restype = None

# /usr/include/mecab.h: 373
if hasattr(_libs['mecab'], 'mecab_get_partial'):
    mecab_get_partial = _libs['mecab'].mecab_get_partial
    mecab_get_partial.argtypes = [POINTER(mecab_t)]
    mecab_get_partial.restype = c_int

# /usr/include/mecab.h: 378
if hasattr(_libs['mecab'], 'mecab_set_partial'):
    mecab_set_partial = _libs['mecab'].mecab_set_partial
    mecab_set_partial.argtypes = [POINTER(mecab_t), c_int]
    mecab_set_partial.restype = None

# /usr/include/mecab.h: 383
if hasattr(_libs['mecab'], 'mecab_get_theta'):
    mecab_get_theta = _libs['mecab'].mecab_get_theta
    mecab_get_theta.argtypes = [POINTER(mecab_t)]
    mecab_get_theta.restype = c_float

# /usr/include/mecab.h: 388
if hasattr(_libs['mecab'], 'mecab_set_theta'):
    mecab_set_theta = _libs['mecab'].mecab_set_theta
    mecab_set_theta.argtypes = [POINTER(mecab_t), c_float]
    mecab_set_theta.restype = None

# /usr/include/mecab.h: 393
if hasattr(_libs['mecab'], 'mecab_get_lattice_level'):
    mecab_get_lattice_level = _libs['mecab'].mecab_get_lattice_level
    mecab_get_lattice_level.argtypes = [POINTER(mecab_t)]
    mecab_get_lattice_level.restype = c_int

# /usr/include/mecab.h: 398
if hasattr(_libs['mecab'], 'mecab_set_lattice_level'):
    mecab_set_lattice_level = _libs['mecab'].mecab_set_lattice_level
    mecab_set_lattice_level.argtypes = [POINTER(mecab_t), c_int]
    mecab_set_lattice_level.restype = None

# /usr/include/mecab.h: 403
if hasattr(_libs['mecab'], 'mecab_get_all_morphs'):
    mecab_get_all_morphs = _libs['mecab'].mecab_get_all_morphs
    mecab_get_all_morphs.argtypes = [POINTER(mecab_t)]
    mecab_get_all_morphs.restype = c_int

# /usr/include/mecab.h: 408
if hasattr(_libs['mecab'], 'mecab_set_all_morphs'):
    mecab_set_all_morphs = _libs['mecab'].mecab_set_all_morphs
    mecab_set_all_morphs.argtypes = [POINTER(mecab_t), c_int]
    mecab_set_all_morphs.restype = None

# /usr/include/mecab.h: 413
if hasattr(_libs['mecab'], 'mecab_parse_lattice'):
    mecab_parse_lattice = _libs['mecab'].mecab_parse_lattice
    mecab_parse_lattice.argtypes = [POINTER(mecab_t), POINTER(mecab_lattice_t)]
    mecab_parse_lattice.restype = c_int

# /usr/include/mecab.h: 418
if hasattr(_libs['mecab'], 'mecab_sparse_tostr'):
    mecab_sparse_tostr = _libs['mecab'].mecab_sparse_tostr
    # mecab_sparse_tostr.argtypes = [POINTER(mecab_t), String]
    # mecab_sparse_tostr.argtypes = [POINTER(mecab_t), POINTER(c_char)]
    mecab_sparse_tostr.argtypes = [POINTER(mecab_t), c_char_p]
    # if sizeof(c_int) == sizeof(c_void_p):
    #     mecab_sparse_tostr.restype = ReturnString
    # else:
    #     mecab_sparse_tostr.restype = String
    #     mecab_sparse_tostr.errcheck = ReturnString
    # mecab_sparse_tostr.restype = c_wchar_p
    mecab_sparse_tostr.restype = c_char_p
# /usr/include/mecab.h: 423
if hasattr(_libs['mecab'], 'mecab_sparse_tostr2'):
    mecab_sparse_tostr2 = _libs['mecab'].mecab_sparse_tostr2
    # mecab_sparse_tostr2.argtypes = [POINTER(mecab_t), String, c_size_t]
    mecab_sparse_tostr2.argtypes = [POINTER(mecab_t), c_char_p, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_sparse_tostr2.restype = ReturnString
    else:
        mecab_sparse_tostr2.restype = String
        mecab_sparse_tostr2.errcheck = ReturnString

# /usr/include/mecab.h: 428
if hasattr(_libs['mecab'], 'mecab_sparse_tostr3'):
    mecab_sparse_tostr3 = _libs['mecab'].mecab_sparse_tostr3
    mecab_sparse_tostr3.argtypes = [POINTER(mecab_t), String, c_size_t, String, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_sparse_tostr3.restype = ReturnString
    else:
        mecab_sparse_tostr3.restype = String
        mecab_sparse_tostr3.errcheck = ReturnString

# /usr/include/mecab.h: 434
if hasattr(_libs['mecab'], 'mecab_sparse_tonode'):
    mecab_sparse_tonode = _libs['mecab'].mecab_sparse_tonode
    mecab_sparse_tonode.argtypes = [POINTER(mecab_t), String]
    mecab_sparse_tonode.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 439
if hasattr(_libs['mecab'], 'mecab_sparse_tonode2'):
    mecab_sparse_tonode2 = _libs['mecab'].mecab_sparse_tonode2
    mecab_sparse_tonode2.argtypes = [POINTER(mecab_t), String, c_size_t]
    mecab_sparse_tonode2.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 444
if hasattr(_libs['mecab'], 'mecab_nbest_sparse_tostr'):
    mecab_nbest_sparse_tostr = _libs['mecab'].mecab_nbest_sparse_tostr
    mecab_nbest_sparse_tostr.argtypes = [POINTER(mecab_t), c_size_t, String]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_nbest_sparse_tostr.restype = ReturnString
    else:
        mecab_nbest_sparse_tostr.restype = String
        mecab_nbest_sparse_tostr.errcheck = ReturnString

# /usr/include/mecab.h: 449
if hasattr(_libs['mecab'], 'mecab_nbest_sparse_tostr2'):
    mecab_nbest_sparse_tostr2 = _libs['mecab'].mecab_nbest_sparse_tostr2
    mecab_nbest_sparse_tostr2.argtypes = [POINTER(mecab_t), c_size_t, String, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_nbest_sparse_tostr2.restype = ReturnString
    else:
        mecab_nbest_sparse_tostr2.restype = String
        mecab_nbest_sparse_tostr2.errcheck = ReturnString

# /usr/include/mecab.h: 455
if hasattr(_libs['mecab'], 'mecab_nbest_sparse_tostr3'):
    mecab_nbest_sparse_tostr3 = _libs['mecab'].mecab_nbest_sparse_tostr3
    mecab_nbest_sparse_tostr3.argtypes = [POINTER(mecab_t), c_size_t, String, c_size_t, String, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_nbest_sparse_tostr3.restype = ReturnString
    else:
        mecab_nbest_sparse_tostr3.restype = String
        mecab_nbest_sparse_tostr3.errcheck = ReturnString

# /usr/include/mecab.h: 462
if hasattr(_libs['mecab'], 'mecab_nbest_init'):
    mecab_nbest_init = _libs['mecab'].mecab_nbest_init
    mecab_nbest_init.argtypes = [POINTER(mecab_t), String]
    mecab_nbest_init.restype = c_int

# /usr/include/mecab.h: 467
if hasattr(_libs['mecab'], 'mecab_nbest_init2'):
    mecab_nbest_init2 = _libs['mecab'].mecab_nbest_init2
    mecab_nbest_init2.argtypes = [POINTER(mecab_t), String, c_size_t]
    mecab_nbest_init2.restype = c_int

# /usr/include/mecab.h: 472
if hasattr(_libs['mecab'], 'mecab_nbest_next_tostr'):
    mecab_nbest_next_tostr = _libs['mecab'].mecab_nbest_next_tostr
    mecab_nbest_next_tostr.argtypes = [POINTER(mecab_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_nbest_next_tostr.restype = ReturnString
    else:
        mecab_nbest_next_tostr.restype = String
        mecab_nbest_next_tostr.errcheck = ReturnString

# /usr/include/mecab.h: 477
if hasattr(_libs['mecab'], 'mecab_nbest_next_tostr2'):
    mecab_nbest_next_tostr2 = _libs['mecab'].mecab_nbest_next_tostr2
    mecab_nbest_next_tostr2.argtypes = [POINTER(mecab_t), String, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_nbest_next_tostr2.restype = ReturnString
    else:
        mecab_nbest_next_tostr2.restype = String
        mecab_nbest_next_tostr2.errcheck = ReturnString

# /usr/include/mecab.h: 482
if hasattr(_libs['mecab'], 'mecab_nbest_next_tonode'):
    mecab_nbest_next_tonode = _libs['mecab'].mecab_nbest_next_tonode
    mecab_nbest_next_tonode.argtypes = [POINTER(mecab_t)]
    mecab_nbest_next_tonode.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 487
if hasattr(_libs['mecab'], 'mecab_format_node'):
    mecab_format_node = _libs['mecab'].mecab_format_node
    mecab_format_node.argtypes = [POINTER(mecab_t), POINTER(mecab_node_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_format_node.restype = ReturnString
    else:
        mecab_format_node.restype = String
        mecab_format_node.errcheck = ReturnString

# /usr/include/mecab.h: 492
if hasattr(_libs['mecab'], 'mecab_dictionary_info'):
    mecab_dictionary_info = _libs['mecab'].mecab_dictionary_info
    mecab_dictionary_info.argtypes = [POINTER(mecab_t)]
    mecab_dictionary_info.restype = POINTER(mecab_dictionary_info_t)

# /usr/include/mecab.h: 498
if hasattr(_libs['mecab'], 'mecab_lattice_new'):
    mecab_lattice_new = _libs['mecab'].mecab_lattice_new
    mecab_lattice_new.argtypes = []
    mecab_lattice_new.restype = POINTER(mecab_lattice_t)

# /usr/include/mecab.h: 503
if hasattr(_libs['mecab'], 'mecab_lattice_destroy'):
    mecab_lattice_destroy = _libs['mecab'].mecab_lattice_destroy
    mecab_lattice_destroy.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_destroy.restype = None

# /usr/include/mecab.h: 508
if hasattr(_libs['mecab'], 'mecab_lattice_clear'):
    mecab_lattice_clear = _libs['mecab'].mecab_lattice_clear
    mecab_lattice_clear.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_clear.restype = None

# /usr/include/mecab.h: 514
if hasattr(_libs['mecab'], 'mecab_lattice_is_available'):
    mecab_lattice_is_available = _libs['mecab'].mecab_lattice_is_available
    mecab_lattice_is_available.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_is_available.restype = c_int

# /usr/include/mecab.h: 519
if hasattr(_libs['mecab'], 'mecab_lattice_get_bos_node'):
    mecab_lattice_get_bos_node = _libs['mecab'].mecab_lattice_get_bos_node
    mecab_lattice_get_bos_node.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_bos_node.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 524
if hasattr(_libs['mecab'], 'mecab_lattice_get_eos_node'):
    mecab_lattice_get_eos_node = _libs['mecab'].mecab_lattice_get_eos_node
    mecab_lattice_get_eos_node.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_eos_node.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 530
if hasattr(_libs['mecab'], 'mecab_lattice_get_all_begin_nodes'):
    mecab_lattice_get_all_begin_nodes = _libs['mecab'].mecab_lattice_get_all_begin_nodes
    mecab_lattice_get_all_begin_nodes.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_all_begin_nodes.restype = POINTER(POINTER(mecab_node_t))

# /usr/include/mecab.h: 534
if hasattr(_libs['mecab'], 'mecab_lattice_get_all_end_nodes'):
    mecab_lattice_get_all_end_nodes = _libs['mecab'].mecab_lattice_get_all_end_nodes
    mecab_lattice_get_all_end_nodes.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_all_end_nodes.restype = POINTER(POINTER(mecab_node_t))

# /usr/include/mecab.h: 539
if hasattr(_libs['mecab'], 'mecab_lattice_get_begin_nodes'):
    mecab_lattice_get_begin_nodes = _libs['mecab'].mecab_lattice_get_begin_nodes
    mecab_lattice_get_begin_nodes.argtypes = [POINTER(mecab_lattice_t), c_size_t]
    mecab_lattice_get_begin_nodes.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 544
if hasattr(_libs['mecab'], 'mecab_lattice_get_end_nodes'):
    mecab_lattice_get_end_nodes = _libs['mecab'].mecab_lattice_get_end_nodes
    mecab_lattice_get_end_nodes.argtypes = [POINTER(mecab_lattice_t), c_size_t]
    mecab_lattice_get_end_nodes.restype = POINTER(mecab_node_t)

# /usr/include/mecab.h: 549
if hasattr(_libs['mecab'], 'mecab_lattice_get_sentence'):
    mecab_lattice_get_sentence = _libs['mecab'].mecab_lattice_get_sentence
    mecab_lattice_get_sentence.argtypes = [POINTER(mecab_lattice_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_lattice_get_sentence.restype = ReturnString
    else:
        mecab_lattice_get_sentence.restype = String
        mecab_lattice_get_sentence.errcheck = ReturnString

# /usr/include/mecab.h: 554
if hasattr(_libs['mecab'], 'mecab_lattice_set_sentence'):
    mecab_lattice_set_sentence = _libs['mecab'].mecab_lattice_set_sentence
    mecab_lattice_set_sentence.argtypes = [POINTER(mecab_lattice_t), String]
    mecab_lattice_set_sentence.restype = None

# /usr/include/mecab.h: 560
if hasattr(_libs['mecab'], 'mecab_lattice_set_sentence2'):
    mecab_lattice_set_sentence2 = _libs['mecab'].mecab_lattice_set_sentence2
    mecab_lattice_set_sentence2.argtypes = [POINTER(mecab_lattice_t), String, c_size_t]
    mecab_lattice_set_sentence2.restype = None

# /usr/include/mecab.h: 565
if hasattr(_libs['mecab'], 'mecab_lattice_get_size'):
    mecab_lattice_get_size = _libs['mecab'].mecab_lattice_get_size
    mecab_lattice_get_size.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_size.restype = c_size_t

# /usr/include/mecab.h: 570
if hasattr(_libs['mecab'], 'mecab_lattice_get_z'):
    mecab_lattice_get_z = _libs['mecab'].mecab_lattice_get_z
    mecab_lattice_get_z.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_z.restype = c_double

# /usr/include/mecab.h: 575
if hasattr(_libs['mecab'], 'mecab_lattice_set_z'):
    mecab_lattice_set_z = _libs['mecab'].mecab_lattice_set_z
    mecab_lattice_set_z.argtypes = [POINTER(mecab_lattice_t), c_double]
    mecab_lattice_set_z.restype = None

# /usr/include/mecab.h: 580
if hasattr(_libs['mecab'], 'mecab_lattice_get_theta'):
    mecab_lattice_get_theta = _libs['mecab'].mecab_lattice_get_theta
    mecab_lattice_get_theta.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_theta.restype = c_double

# /usr/include/mecab.h: 586
if hasattr(_libs['mecab'], 'mecab_lattice_set_theta'):
    mecab_lattice_set_theta = _libs['mecab'].mecab_lattice_set_theta
    mecab_lattice_set_theta.argtypes = [POINTER(mecab_lattice_t), c_double]
    mecab_lattice_set_theta.restype = None

# /usr/include/mecab.h: 591
if hasattr(_libs['mecab'], 'mecab_lattice_next'):
    mecab_lattice_next = _libs['mecab'].mecab_lattice_next
    mecab_lattice_next.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_next.restype = c_int

# /usr/include/mecab.h: 596
if hasattr(_libs['mecab'], 'mecab_lattice_get_request_type'):
    mecab_lattice_get_request_type = _libs['mecab'].mecab_lattice_get_request_type
    mecab_lattice_get_request_type.argtypes = [POINTER(mecab_lattice_t)]
    mecab_lattice_get_request_type.restype = c_int

# /usr/include/mecab.h: 601
if hasattr(_libs['mecab'], 'mecab_lattice_has_request_type'):
    mecab_lattice_has_request_type = _libs['mecab'].mecab_lattice_has_request_type
    mecab_lattice_has_request_type.argtypes = [POINTER(mecab_lattice_t), c_int]
    mecab_lattice_has_request_type.restype = c_int

# /usr/include/mecab.h: 606
if hasattr(_libs['mecab'], 'mecab_lattice_set_request_type'):
    mecab_lattice_set_request_type = _libs['mecab'].mecab_lattice_set_request_type
    mecab_lattice_set_request_type.argtypes = [POINTER(mecab_lattice_t), c_int]
    mecab_lattice_set_request_type.restype = None

# /usr/include/mecab.h: 612
if hasattr(_libs['mecab'], 'mecab_lattice_add_request_type'):
    mecab_lattice_add_request_type = _libs['mecab'].mecab_lattice_add_request_type
    mecab_lattice_add_request_type.argtypes = [POINTER(mecab_lattice_t), c_int]
    mecab_lattice_add_request_type.restype = None

# /usr/include/mecab.h: 617
if hasattr(_libs['mecab'], 'mecab_lattice_remove_request_type'):
    mecab_lattice_remove_request_type = _libs['mecab'].mecab_lattice_remove_request_type
    mecab_lattice_remove_request_type.argtypes = [POINTER(mecab_lattice_t), c_int]
    mecab_lattice_remove_request_type.restype = None

# /usr/include/mecab.h: 622
if hasattr(_libs['mecab'], 'mecab_lattice_tostr'):
    mecab_lattice_tostr = _libs['mecab'].mecab_lattice_tostr
    mecab_lattice_tostr.argtypes = [POINTER(mecab_lattice_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_lattice_tostr.restype = ReturnString
    else:
        mecab_lattice_tostr.restype = String
        mecab_lattice_tostr.errcheck = ReturnString

# /usr/include/mecab.h: 627
if hasattr(_libs['mecab'], 'mecab_lattice_tostr2'):
    mecab_lattice_tostr2 = _libs['mecab'].mecab_lattice_tostr2
    mecab_lattice_tostr2.argtypes = [POINTER(mecab_lattice_t), String, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_lattice_tostr2.restype = ReturnString
    else:
        mecab_lattice_tostr2.restype = String
        mecab_lattice_tostr2.errcheck = ReturnString

# /usr/include/mecab.h: 632
if hasattr(_libs['mecab'], 'mecab_lattice_nbest_tostr'):
    mecab_lattice_nbest_tostr = _libs['mecab'].mecab_lattice_nbest_tostr
    mecab_lattice_nbest_tostr.argtypes = [POINTER(mecab_lattice_t), c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_lattice_nbest_tostr.restype = ReturnString
    else:
        mecab_lattice_nbest_tostr.restype = String
        mecab_lattice_nbest_tostr.errcheck = ReturnString

# /usr/include/mecab.h: 638
if hasattr(_libs['mecab'], 'mecab_lattice_nbest_tostr2'):
    mecab_lattice_nbest_tostr2 = _libs['mecab'].mecab_lattice_nbest_tostr2
    mecab_lattice_nbest_tostr2.argtypes = [POINTER(mecab_lattice_t), c_size_t, String, c_size_t]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_lattice_nbest_tostr2.restype = ReturnString
    else:
        mecab_lattice_nbest_tostr2.restype = String
        mecab_lattice_nbest_tostr2.errcheck = ReturnString

# /usr/include/mecab.h: 643
if hasattr(_libs['mecab'], 'mecab_lattice_strerror'):
    mecab_lattice_strerror = _libs['mecab'].mecab_lattice_strerror
    mecab_lattice_strerror.argtypes = [POINTER(mecab_lattice_t)]
    if sizeof(c_int) == sizeof(c_void_p):
        mecab_lattice_strerror.restype = ReturnString
    else:
        mecab_lattice_strerror.restype = String
        mecab_lattice_strerror.errcheck = ReturnString

# /usr/include/mecab.h: 650
if hasattr(_libs['mecab'], 'mecab_model_new'):
    mecab_model_new = _libs['mecab'].mecab_model_new
    mecab_model_new.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_model_new.restype = POINTER(mecab_model_t)

# /usr/include/mecab.h: 655
if hasattr(_libs['mecab'], 'mecab_model_new2'):
    mecab_model_new2 = _libs['mecab'].mecab_model_new2
    mecab_model_new2.argtypes = [String]
    mecab_model_new2.restype = POINTER(mecab_model_t)

# /usr/include/mecab.h: 661
if hasattr(_libs['mecab'], 'mecab_model_destroy'):
    mecab_model_destroy = _libs['mecab'].mecab_model_destroy
    mecab_model_destroy.argtypes = [POINTER(mecab_model_t)]
    mecab_model_destroy.restype = None

# /usr/include/mecab.h: 666
if hasattr(_libs['mecab'], 'mecab_model_new_tagger'):
    mecab_model_new_tagger = _libs['mecab'].mecab_model_new_tagger
    mecab_model_new_tagger.argtypes = [POINTER(mecab_model_t)]
    mecab_model_new_tagger.restype = POINTER(mecab_t)

# /usr/include/mecab.h: 671
if hasattr(_libs['mecab'], 'mecab_model_new_lattice'):
    mecab_model_new_lattice = _libs['mecab'].mecab_model_new_lattice
    mecab_model_new_lattice.argtypes = [POINTER(mecab_model_t)]
    mecab_model_new_lattice.restype = POINTER(mecab_lattice_t)

# /usr/include/mecab.h: 676
if hasattr(_libs['mecab'], 'mecab_model_swap'):
    mecab_model_swap = _libs['mecab'].mecab_model_swap
    mecab_model_swap.argtypes = [POINTER(mecab_model_t), POINTER(mecab_model_t)]
    mecab_model_swap.restype = c_int

# /usr/include/mecab.h: 681
if hasattr(_libs['mecab'], 'mecab_model_dictionary_info'):
    mecab_model_dictionary_info = _libs['mecab'].mecab_model_dictionary_info
    mecab_model_dictionary_info.argtypes = [POINTER(mecab_model_t)]
    mecab_model_dictionary_info.restype = POINTER(mecab_dictionary_info_t)

# /usr/include/mecab.h: 684
if hasattr(_libs['mecab'], 'mecab_do'):
    mecab_do = _libs['mecab'].mecab_do
    mecab_do.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_do.restype = c_int

# /usr/include/mecab.h: 685
if hasattr(_libs['mecab'], 'mecab_dict_index'):
    mecab_dict_index = _libs['mecab'].mecab_dict_index
    mecab_dict_index.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_dict_index.restype = c_int

# /usr/include/mecab.h: 686
if hasattr(_libs['mecab'], 'mecab_dict_gen'):
    mecab_dict_gen = _libs['mecab'].mecab_dict_gen
    mecab_dict_gen.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_dict_gen.restype = c_int

# /usr/include/mecab.h: 687
if hasattr(_libs['mecab'], 'mecab_cost_train'):
    mecab_cost_train = _libs['mecab'].mecab_cost_train
    mecab_cost_train.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_cost_train.restype = c_int

# /usr/include/mecab.h: 688
if hasattr(_libs['mecab'], 'mecab_system_eval'):
    mecab_system_eval = _libs['mecab'].mecab_system_eval
    mecab_system_eval.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_system_eval.restype = c_int

# /usr/include/mecab.h: 689
if hasattr(_libs['mecab'], 'mecab_test_gen'):
    mecab_test_gen = _libs['mecab'].mecab_test_gen
    mecab_test_gen.argtypes = [c_int, POINTER(POINTER(c_char))]
    mecab_test_gen.restype = c_int

mecab_dictionary_info_t = struct_mecab_dictionary_info_t # /usr/include/mecab.h: 15

mecab_node_t = struct_mecab_node_t # /usr/include/mecab.h: 98

mecab_path_t = struct_mecab_path_t # /usr/include/mecab.h: 62

mecab_t = struct_mecab_t # /usr/include/mecab.h: 334

mecab_model_t = struct_mecab_model_t # /usr/include/mecab.h: 335

mecab_lattice_t = struct_mecab_lattice_t # /usr/include/mecab.h: 336

# No inserted files

# ###################################

def whitespace(s):
    argc = c_int(2)
    tagger = mecab_new2(b"-E '' -O wakati")
    g = mecab_sparse_tostr(tagger, s)
    mecab_destroy(tagger)
    g=g.strip()
    return g

if __name__ == "__main__":
    s="alex madon 本日は晴天なり"
    print(s,'=>')
    res=whitespace(s.encode('utf8'))
    print(res.decode('utf8'))
