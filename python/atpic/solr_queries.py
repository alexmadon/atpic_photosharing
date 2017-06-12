"""returns the solr URLs """

# cd /home/madon/solr/apache-solr-1.3.0/example

# rm -rf solr/data/
# java -jar start.jar


def get_pics(aid,day):
    
    # http://localhost:8983/solr/select/?q=*:*
    # http://localhost:8983/solr/select/?q=aid:1
    # http://localhost:8983/solr/select/?q=date:

    # send 100 results 
    # http://localhost:8983/solr/select/?q=aid:1&start=50&rows=100

    # outputs only the fields "pid" and "gid" with paging
    # http://localhost:8983/solr/select/?q=aid:1&start=50&rows=100&fl=pid+gid
    # or with commas
    # http://localhost:8983/solr/select/?q=aid:1&start=50&rows=100&fl=pid,gid
    # or with sort
    # http://localhost:8983/solr/select/?q=aid:1&start=51&rows=3&fl=pid,gid,score&sort=pid+asc

 



    # for dates see: http://wiki.apache.org/solr/SolrQuerySyntax
    # note: in ranges TO needs to be CAPITAL letters
    # http://localhost:8983/solr/select/?q=date:[2004-06-02T00:00:00.000Z TO 2004-06-04T00:00:00.000Z]&fl=date+pid+gid
   # http://localhost:8983/solr/select/?q=date:2007-05-30T12:34:56Z


    # http://localhost:8983/solr/select/?q=date:[2004-06-02T00:00:00.000Z TO 2004-06-04T00:00:00.000Z]&fl=date+pid+gid&sort=date desc


    # random pictures
    # use the randomfields in sort
    # http://localhost:8983/solr/select/?q=aid:20&sort=random50 desc&fl=pid


    # first picturs in gallery
    # http://localhost:8983/solr/select/?q=gid:8432
    # http://localhost:8983/solr/select/?q=childof:8432
    # http://localhost:8983/solr/select/?q=childof:8432 depth8432:2&fl=pid gid depth8432&rows=100
    # http://localhost:8983/solr/select/?q=childof:8432 depth8432:2&sort=depth8432 desc&fl=pid gid depth8432&rows=1
    # http://localhost:8983/solr/select/?q=childof:8432&sort=depth8432 asc&fl=pid gid depth8432&rows=1


    # latitude, geolocalisation
    # http://localhost:8983/solr/select/?q=glat:[30 TO 50]
    # http://localhost:8983/solr/select/?q=lat:[30 TO 50]



    # http://localhost:8983/solr/select/?q=year:2006
    # http://localhost:8983/solr/select/?q=yearmonth:200601
    # http://localhost:8983/solr/select/?q=yearmonthday:20060131





    # faceting by date (photoblog) : the facet.field=date seems WRONG
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=date&facet.date=date&facet.date.start=NOW/DAY-12500DAYS&facet.date.end=NOW/DAY%2B1DAY&facet.date.gap=%2B1DAY


    # for one month, no facet fields
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.date=date&facet.date.start=NOW/DAY-19MONTH&facet.date.end=NOW/DAY-18MONTH&facet.date.gap=%2B1DAY

    # for an absolute given date interval, one month, no facet fields
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.date=date&facet.date.start=2005-06-29T00:00:00Z&facet.date.end=2006-06-29T00:00:00Z&facet.date.gap=%2B1DAY



    
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=tag
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=tag&facet.prefix=a
    
    
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=make
    
    
    # http://localhost:8983/solr/select/?q=*:*&rows=0&facet=true&facet.field=model






    # luke
    # http://wiki.apache.org/solr/LukeRequestHandler

    # http://localhost:8983/solr/admin/luke?id=p100
    # http://localhost:8983/solr/admin/luke?id=p2671 has lierre &amp; pierre inptitle 
    # http://localhost:8983/solr/select/?q=ptitle:lierre



    # http://localhost:8983/solr/select/?q=gtitle:macro aid:1
    # differs from
    # http://localhost:8983/solr/select/?q=gtitle:Macro aid:1

    
    # because SOLR does not support "select distinct"
    # we will need to mark as first in gallery


    # ########################################
    #    NEW
    # ########################################
    # http://localhost:8983/solr/select?q=*:*

    # http://localhost:8983/solr/select?q=user:1&group=true&group.field=useryear
    # http://localhost:8983/solr/select?q=useryear:12010*&group=true&group.field=useryearmonth
    # http://localhost:8983/solr/select?q=useryearmonth:1200310&group=true&group.field=useryearmonthday
    # http://localhost:8983/solr/select?q=useryearmonth:1200310&group=true&group.field=useryearmonthday&sort=useryearmonthday
    # http://localhost:8983/solr/select?q=useryearmonth:1200310&group=true&group.field=useryearmonthday&sort=useryearmonthday+desc


    # http://localhost:8983/solr/select?q=gallery:3+OR+gallery:4+OR+gallery:17733&group=true&group.field=gallery
    # http://localhost:8983/solr/select?q=user:1&group=true&group.field=gallery
    # http://localhost:8983/solr/select?q=user:1+dir:48542&group=true&group.field=gallery BAD
    # http://localhost:8983/solr/select?q=user:1+dir_0:48542&group=true&group.field=gallery&sort=path+desc GOOD
    # http://localhost:8983/solr/select?q=user:1+dir_0:48542&group=true&group.field=dir_1&sort=path+desc
    # http://localhost:8983/solr/select?q=*:*&sort=random_15+desc'
