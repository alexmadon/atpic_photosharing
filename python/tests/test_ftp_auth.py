# sql ftp auth
select getpasswdfromlogin('alexmadon','user2.atpic.com');
select getpasswdfromlogin('alexmadon','user.atpic.foo');

select getdirfromlogin('alexmadon');

select * from getquotalogin('alexmadon');
select * from getquotalogin('alexmadon2');
