create table test5 (i int, j int default i);
create table test5 (i int, j int default (select min(i)));
