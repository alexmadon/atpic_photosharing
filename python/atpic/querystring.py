# BASIC presentation:
# GET methods:
# http://atpic.com/pic?q=uid:1&page=1
# http://atpic.com/pic/99?q=uid:1&row=100 (need next and previous links)


# http://atpic.com/pic?q=gid:54&page=1
# http://atpic.com/pic/99?q=gid:54&row=100 (need next and previous links)
# http://atpic.com/pic/99  (no next and previous links, but link to gallery and user)

# http://atpic.com/pic?q=france
# http://atpic.com/pic?q=france&page=1
# http://atpic.com/pic/99?q=france&row=100 (same as http://atpic.com/pic/99 but with nav)
# http://atpic.com/pic/99.xml
# http://atpic.com/pic/99?format=xml

#===========================
# ADMIN page:
# http://alex.atpic.com/_admin
# http://alex.atpic.com/_ftp
# http://alex.atpic.com/_login
# http://atpic.com/login

#==================================
# another scheme: PATH: (need DNS as tree is local to server) 
# (can use webdav too, ftp)
# http://alex.atpic.com/france/paris
# http://alex.atpic.com/france/paris?page=1

# http://atpic.com/alex/france/paris
# http://atpic.com/alex/france/paris?page=1

# http://alex.dav.atpic.com/france/paris
# http://u1.udav.atpic.com/france/paris

#==================================
# another scheme: BLOG (blog)
# http://blog.atpic.com/2009/12/31
# http://atpic.com/blog/2009/12/31
# http://alex.blog.atpic.com/2009/12/31
# http://blog.atpic.com/alex/2009/12/31
# http://atpic.com/blog/alex/2009/12/31
# http://atpic.com/blog/2009/12/31?uid=1
# http://atpic.com/blog/2009/12/31?name=alex
# http://atpic.com/blog/2009/12/31/alex
# http://atpic.com/alex@2009/12/31
# http://atpic.com/alex/_2009/12/31   ***good***
# http://atpic.com/alex/_2009/12      ***good***
# http://atpic.com/alex/_2009         ***good***

# OR say that blog is the default behaviour:

# http://atpic.com/alex  (last pictures, last comments) *** better ***
# http://atpic.com/alex/2009                            *** better ***
# http://atpic.com/alex/2009/12                         *** better ***
# http://atpic.com/alex/2009/12/31                      *** better ***

# and do PATH only in http://alex.atpic.com/

#==================================
# FORGET about TAG:
# another scheme: TAG (tag)
# http://tag.atpic.com/ 
# http://tag.atpic.com/france 


# http://alex.tag.atpic.com/ (cloud)
# http://alex.tag.atpic.com/france (cloud)

