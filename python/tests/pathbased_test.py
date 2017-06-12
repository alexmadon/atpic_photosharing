#!/usr/bin/python3
import unittest


import atpic.pathbased
import atpic.redis_pie
import atpic.fuse3pathbased

class Path(unittest.TestCase):
    """USER legacy urls"""

    def NOtest_sql(self):
        db=atpic.libpqalex.db()

        paths=(
            (b'alex/avignon/dama',),
            (b'alex/avignon/dama/picdoesnotexist.jpg',),
            (b'alex/avignon/dirdoesnoexist',),
            )
        for apath in paths:
            path=apath[0]
            res=atpic.pathbased.sql_stat_path(path,db)
            print('XXXX',path,res)

    def NOtest_path_split(self):

        paths=(
            (b'/',(b's', ())),
            (b'/alex',(b'u', b'alex')),
            (b'/alex/avignon',(b'g', (b'alex', b'/avignon'))),
            (b'/alex/av',(b'g', (b'alex', b'/av'))),
            (b'/alex/19',(b'g', (b'alex', b'/19'))),
            (b'/alex/1',(b'g', (b'alex', b'/1'))),
            (b'/alex/avignon/dama',(b'g', (b'alex', b'/avignon/dama'))),
            (b'/alex/avignon/dama/picdoesnotexist.jpg',(b'p', (b'alex', b'/avignon/dama', b'picdoesnotexist.jpg'))),
            (b'/alex/avignon/dirdoesnoexist',(b'g', (b'alex', b'/avignon/dirdoesnoexist'))),
            (b'/alex/pic.jpg',(b'p', (b'alex', b'/', b'pic.jpg'))),
            )

        i=0
        for (apath,res_ex) in paths:
            i=i+1
            print('++++',i,'+++++')
            path=apath
            res=atpic.pathbased.path_split(path)
            print('XXXX (',path,',',res,'),',sep='')
            self.assertEqual(res_ex,res)


    def NOtest_get_uidpartition_redis(self):
        rediscon=atpic.redis_pie.Redis()

        uname=b'alex'
        # init redis to force a None
        rediscon._del(b'n_'+uname)
        uidpartition=atpic.pathbased.get_uidpartition_redis(uname,rediscon)
        print('uidpartition Redis',uidpartition)
        self.assertEqual(uidpartition,None)

        # force a SQL
        uidpartition=atpic.pathbased.get_uidpartition_sql(uname)
        print('uidpartition SQL',uidpartition)

        self.assertEqual(uidpartition,(b'1', b'/hdc1'))

        (uid,partition)=uidpartition
        # set redis
        atpic.pathbased.set_uidpartition_redis(uname,uid,partition,rediscon)

        # call redis again
        uidpartition=atpic.pathbased.get_uidpartition_redis(uname,rediscon)
        print('uidpartition Redis',uidpartition)
        self.assertEqual(uidpartition,(b'1', b'/hdc1'))
        rediscon.quit()



    def NOtest_get_uidpartition_redis(self):
        rediscon=atpic.redis_pie.Redis()

        uid=b'1'
        dirpath=b'/test3'

        rediscon._del(b'u_'+uid)

        gidmtime=atpic.pathbased.get_gid_redis(uid,dirpath,rediscon)
        print('gidmtime',gidmtime)
        self.assertEqual(gidmtime,None)

        result=atpic.pathbased.sql_get_user_tree(uid)
        atpic.pathbased.set_tree_redis(uid,result,rediscon)

        gidmtime=atpic.pathbased.get_gid_redis(uid,dirpath,rediscon)
        print('gidmtimeredis',gidmtime)
        rediscon.quit()

    def NOtest_listdir_sql(self):

        # 48542
        result=atpic.pathbased.listdir_sql(b'1',b'48542')
        print(result)
        alist=atpic.pathbased.get_dirnames(result)
        print(alist)


if __name__=="__main__":

    unittest.main()
