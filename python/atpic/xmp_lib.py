import sys
import os
import os.path

sys.path.append(os.path.pardir)

from libxmp import *
from libxmp.core import XMPIterator


def tests_xmp_core():
	# XMPFiles.initialize()
	xmpfile = XMPFiles()
	# xmpfile.open_file('../tests/fixture/xmp/sig05-002a.tif',files.XMP_OPEN_READ )
	xmpfile.open_file('../tests/fixture/xmp/sig05-002a.tif')
	# print dir(xmpfile)
	xmp = xmpfile.get_xmp()
	print(dir(xmp))
	xmp.register_namespace("http://atpic.com/atxmp/1.0/avm/1.0/","atpic")
	print(xmp.set_property("http://atpic.com/atxmp/1.0/avm/1.0/","Publisher","Alex Madon"))
	print(xmp.get_property("http://atpic.com/atxmp/1.0/avm/1.0/","Publisher"))
	quit()
	print(xmp.set_property("http://www.communicatingastronomy.org/avm/1.0/","Publisher","Eric Idle"))
	print(xmp.get_property("http://www.communicatingastronomy.org/avm/1.0/","Publisher"))


	for x in xmp:
		print(x)
		# x.encode("utf8")

#   File "/usr/local/lib/python3.1/dist-packages/libxmp/core.py", line 754, in __next__
#     return (str(schema_ns),str(prop_name),str(prop_value), opts)
# TypeError: __str__ returned non-string (type bytes)
# Solution: remove the str()

	# quit()
	# print the serialization
	print(xmp.serialize_and_format(use_compact_format=True, omit_packet_wrapper=True))



	xmpfile.close_file()
	# XMPFiles.terminate()



tests_xmp_core()
