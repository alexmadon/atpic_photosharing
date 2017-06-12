import atpic.libpqalex


db=atpic.libpqalex.db()
query="insert into test (description) values ($1)"
ps=atpic.libpqalex.pq_prepare(db,'',query)
atext="alex' madon" # no need to escape
result=atpic.libpqalex.pq_exec_prepared(db,'',(atext,))
result=atpic.libpqalex.process_result(result)

