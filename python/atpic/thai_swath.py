#!/usr/bin/python3

# http://www.thai-language.com/id/801644

# แล้วพบกันใหม่ means "See you later."

# and is compound by three words:
# แล้ว
# พบกัน
# ใหม่
# swath - Thai word segmentation program


# echo "แล้วพบกันใหม่" | swath -u u,u -b '#'
# echo "แล้วพบกันใหม่" | swath -u u,u
# แล้ว|พบ|กัน|ใหม่|
# echo "แล้วพบกันใหม่" | swath -u u,u -b ' '

import subprocess

# http://stackoverflow.com/questions/163542/python-how-do-i-pass-a-string-into-subprocess-popen-using-the-stdin-argument

def whitespace(atext):
    process = subprocess.Popen(['swath', '-u', 'u,u', '-b',' '], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate(input=atext)
    stdout=stdout.strip()
    # return (stdout, stderr)
    return stdout
# p = Popen(['grep', 'f'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
# grep_stdout = p.communicate(input='one\ntwo\nthree\nfour\nfive\nsix\n')[0]
# print(grep_stdout)

if __name__ == "__main__":
    a="แล้วพบกันใหม่"
    b=a.encode('utf8')
    c=whitespace(b)
    print(a,'=>',c.decode('utf8'))
