#!/usr/bin/python3

# NOTE: use the '-d' to debug!!!!



# echo '个性化首页 · 网络历史记录' | adso -g chinese.grammar -n
# adso -g chinese.grammar -n -i '个性化首页 · 网络历史记录'

# adso -i '个性化首页 · 网络历史记录' --extra-code "<REDUCE> AND <PRINT chinese_utf8s> AND <PRINT  > AND <IF><CLASS Terminal></IF><THEN><PRINT newline></THEN>"


# adso -i '个性化首页 · 网络历史记录' --extra-code "<REDUCE> AND <PRINT chinese_utf8s> AND <PRINT  > AND <IF><CLASS Punctuation></IF><THEN><PRINT XXXXX></THEN>" 


# adso -i '个性化首页 · 网络历史记录' --extra-code "<REDUCE> AND <PRINT chinese_utf8s> AND <PRINT  >"

# adso -i '个性化首页 · 网络历史记录' --extra-code "<REDUCE> AND <IF><CLASS Noun></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"

# adso -i 'Cet été-là 个性化首页 · 网络历史记录' --extra-code "<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"

# PROBLEM!!!!!! Do not send japanese to adso!!!
# adso -i 'Japanese プライバシーと利用規約' --extra-code "<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"


# adso -i 'แล้วพบกันใหม่' --extra-code "<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"


# adso -i '《國際法院規約》' --extra-code "<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"

# adso -i "翻訳や I'm Feeling Lucky などの特殊な検索機能 " --extra-code "<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"

# -ie gb2312
# -ie utf8
import subprocess

def whitespace(atext):
    # adso -i '《國際法院規約》' --extra-code "<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"
    process = subprocess.Popen(['adso', '-i', atext, '--extra-code',"<REDUCE> AND <IF><NOTCLASS Punctuation></IF><THEN><PRINT chinese_utf8s> AND <PRINT  ></THEN>"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    stdout, stderr = process.communicate(input=atext)
    stdout=stdout.strip()
    # return (stdout, stderr)
    return stdout

if __name__ == "__main__":
    a='个性化首页 · 网络历史记录'
    print(a)
    b=whitespace(a.encode('utf8'))
    print(b.decode('utf8'))
    # 个性化首页 · 网络历史记录
    # returns: 个性化 首页 网络 历史记录
