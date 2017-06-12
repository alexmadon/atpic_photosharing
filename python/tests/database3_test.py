import atpic.libpqalex

db=atpic.libpqalex.db()
a=db.atpicdb.pic_list()
print(a)
print("=================")
print(type(a))
print("=================")
print(dir(db.atpicdb))
print("=================")
print(dir(db))
