# cookies libary to process
# lang, format, resolution, wiki
# file:///home/madon/doc/python-3.3a0-docs-html/library/http.cookies.html

from http import cookies
C = cookies.SimpleCookie()
C["fig"] = "newton"
C["sugar"] = "wafer"
print(C)

C = cookies.SimpleCookie()
C["rocky"] = "road"
C["rocky"]["path"] = "/cookie"
print(C.output(header="Cookie:"))
print(C["rocky"].value)
print(C.output(header=''))
print(dir(C["rocky"]))
print(C["rocky"].values())
print(C["rocky"].output())
print(C["rocky"].coded_value)
print(C["rocky"].OutputString())


C = cookies.SimpleCookie()
C.load("chips=ahoy; vienna=finger")
print(C.keys())
