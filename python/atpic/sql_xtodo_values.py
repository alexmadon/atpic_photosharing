# need to clean servershot:
# there are some servershot that are empty, are only digits, have no ascii:
# require at least one character in [a-z]

# if not, then copy from admin_login

# atpic.com/uname
# atpic.com/pic -> reserved words
# atpic.com/2009 -> blog

# no _ as first character of 'file' (directory name)
# mydbserver=# select id,file from artist_gallery where file like '\\_%' order by id; 
#   id   | file  
# -------+-------
#  20877 | _____
# (1 row)

