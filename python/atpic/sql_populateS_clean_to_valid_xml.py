#!/usr/bin/python3
"""Clean the DB to be able to send clean XML to solr directly from SQL"""

import atpic.libpqalex
import atpic.cleaner
import types
import difflib
import atpic.mybytes
import atpic.log
import atpic.simplediff

xx=atpic.log.setmod("INFO","clean1")



def clean_table_txt(table,query,cleaner_function):
    """transforms XML fields (in particular thetitle, thetext) to TXT"""
    yy=atpic.log.setname(xx,'clean_table_txt')

    atpic.log.info(yy,'input=',(table,query,cleaner_function))
    db=atpic.libpqalex.db()
    hasmore=1
    thelimit=100
    
    ps=atpic.libpqalex.pq_prepare(db,b'',query)
    counter=0
    offset=b'0'
    while (hasmore> 0):
        bthelimit=atpic.mybytes.int2bytes(thelimit)
        boffset=offset
        result=atpic.libpqalex.pq_exec_prepared(db,b'',(boffset,bthelimit,))
        result=atpic.libpqalex.process_result(result)
        listofdict=result # result.dictresult()
        rows=len(listofdict)
        if rows< thelimit:
            hasmore=0
        else:
            counter=counter+1
        i=0
        for adict in listofdict:
            i=i+1
            offset=adict[b"id"]
            for (k,v) in list(adict.items()):
                atpic.log.debug(yy,'kv=',k,v)
                
                # cleaned_value=atpic.cleaner.html(v)
                cleaned_value=cleaner_function(v)

                if v!=cleaned_value:
                    atpic.log.info(yy,'+++++++++++++++++++++++++++++++++++++++++++')
                    atpic.log.info(yy,'differs OLDDDD=',v.decode('utf8'),'NEWWWW=',cleaned_value.decode('utf8'),'EEEEEND')
                    thediff=atpic.simplediff.string_diff(v,cleaned_value)
                    # atpic.log.info(yy,'diff',thediff)
                    for (sign,alist) in thediff:
                        if sign!='=':
                            atpic.log.info(yy,'diff=',(sign,alist))
                    # you need to create a list of strings [,]
                    # thediff=difflib.ndiff([v.decode('utf8'),],[cleaned_value.decode('utf8'),])
                    # thediff2='difference='.join(list(thediff))
                    # atpic.log.debug(yy,'difference=',thediff2)
                    atpic.log.debug(yy,'DIFFER! i=',i,'id=',adict[b"id"])

                    cleaned_value_sql=cleaned_value.replace(b"'",b"''")
                    sql=b"update "+table+b" set "+k+b"='"+cleaned_value_sql+b"' where id='"+adict[b"id"]+b"';"
                    print(sql.decode('utf8'))












if __name__ == "__main__":
    # clean_table("artist_gallery")
    # clean_table("artist")
    # clean_table("artist_pic")

    # clean_table_txt("artist")
    # clean_table_txt("artist_gallery")
    # clean_table_txt("artist_pic")

    # NEW:
    # clean_table_txt(b"_user_gallery_pic",b"_title",b"_text")
    # clean_table_txt(b"_user_gallery",b"_title",b"_text")
    # clean_table_txt(b"_user",b"_title",b"_text")

    table_list=[b"_user",b"_user_gallery",b"_user_gallery_pic"]
    # table_list=[b"_user_gallery",b"_user_gallery_pic",]

    # atpic.cleaner.html for XML
    # atpic.cleaner.txt for TXT
    cleaner_function=getattr(atpic.cleaner,"html")
    for table in table_list:
        query=b"select id,_title,_text from "+table+b" where ((_title!='' and _title!=' ') or (_text!='' and _text!=' ')) and id>$1 order by id limit $2"
        # query=b"select id,_title,_text from "+table+b" where id>$1 order by id limit $2"

        print('--',query)
        clean_table_txt(table, query,cleaner_function)
