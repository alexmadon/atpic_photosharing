#!/usr/bin/python3

import subprocess

def convert(atext):
    # convert to HTML
    # pandoc -f mediawiki test.mdwn
    # then process HTML
    # p1 = Popen(["dmesg"], stdout=PIPE)
    # p2 = Popen(["grep", "hda"], stdin=p1.stdout, stdout=PIPE)
    # p1.stdout.close()  # Allow p1 to receive a SIGPIPE if p2 exits.
    # output = p2.communicate()[0]
    
    p1 = subprocess.Popen(["pandoc", "-f", "mediawiki"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
# output = p1.communicate()[0]
    (stdout, stderr) = p1.communicate(input=atext)
    return(stdout, stderr)



if __name__=="__main__":
    atext=b"""
[[google]] is wiki

- one
- two


* ONE
* TWO

* uno
* dos
** tres

soome *bold* face
''double'' done

<m>mmmm</m>
"""
    (out,err)=convert(atext)
    print(out)
