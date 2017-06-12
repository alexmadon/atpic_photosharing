# ext3 needs to be mounted with option user_xattr

import xattr
xattr.listxattr("file.txt")
xattr.setxattr("file.txt", "user.comment", "Simple text file")
xattr.getxattr("file.txt", "user.comment")
