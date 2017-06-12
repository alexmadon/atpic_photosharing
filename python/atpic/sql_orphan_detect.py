#!/usr/bin/python3
print("""

-- select * from _user_gallery as UG where _dir not in (select id from _user_gallery where _user=UG._user);
select id,_user,_isroot,_dir from _user_gallery as UG where _dir>0 and _dir is not null and _dir not in (select id from _user_gallery where _user=UG._user);
""")


"""
  id   | _user | _isroot | _dir  
-------+-------+---------+-------
 33375 |  7332 | n       | 33104
 26548 |  5805 | n       | 26867
 19779 |  1503 | n       |  6416
 48107 | 11381 | n       | 48105
 26547 |  5805 | n       | 26867
 33201 |  7332 | n       | 33104
 21890 |  2220 | n       | 21889
 21891 |  2220 | n       | 21889
 33105 |  7332 | n       | 33104
 28457 |  5464 | n       | 23585
 31319 |  5464 | n       | 23585
 32855 |  7201 | n       | 32314
 37444 |  5464 | n       | 23585
 36447 |  4962 | n       | 29276
 25564 |  1485 | n       | 25563
 16946 |   797 | n       | 13628
 32838 |  7201 | n       | 32314
 36825 |  7853 | n       | 36370
 14802 |   797 | n       | 14241
(19 rows)
"""
