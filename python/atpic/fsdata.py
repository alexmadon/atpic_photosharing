# server side FUSE filesystem
# this implements all FUSE  functions

"""
Forge XML messages based on  the data of Solr

It is then called and processed by the fuse module




"""

def dummy(dispatcher,environ):
    return """<message>
Path: %s
Filesystem action '%s' is not implemented

</message>




""" % (dispatcher["path"],dispatcher["fsaction"])



# some helper functions

def break_path(path):
    """Breaks a full path is username, dir(s), file"""









# Now the fuse functions

def getattr(dispatcher,environ):
    """gets he attr for path dispatcher["path"]"""
    out=[]
    out.append("""<message>""")
    out.append("""<path>%s</path>""" % dispatcher["path"])
    out.append("""<action>%s</action>""" % dispatcher["fsaction"])
    # getting the data SQL or Solr
    # should say if exists (if it does not exist send an error)
    # if exists: gives the type (dir or file)
    out.append("""</message>""")

    return "".join(out)


def readlink(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def readdir(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def unlink(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def rmdir(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def symlink(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def rename(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def link(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def chmod(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def chown(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def truncate(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def mknod(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def mkdir(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def utime(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def access(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def read(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


def write(dispatcher,environ):
    out=[]
    out.append("""<message>
<path>%s</path>
<action>%s</action>
</message>
""" % (dispatcher["path"],dispatcher["fsaction"]))
    return "".join(out)


