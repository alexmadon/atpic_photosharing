# sample log line format:
# 2008-08-14T08:40:49+00:00 user4 httpd: AJAXC,p,1009173

# requires ts_format(iso); in syslog-ng
# /etc/syslog-ng/syslog-ng.conf
# options {
#        ts_format(iso);  # use ISO8601 timestamps


# port of /shells/ajax_clean.pl


# select count(id) as thecount,type,id from ajaxc group by type,id order by thecount desc;
#syslog-ng ts_format(iso); # use ISO8601 timestamps
#example:
#2007-06-02T05:19:11+05:00
#http://www.cl.cam.ac.uk/~mgk25/iso-time.html
#http://www.ietf.org/rfc/rfc3339.txt
#[madon@debi shells]$ date +"%Y-%m-%d"
#2007-06-05



#move data from tables to ajaxctmp
#JUST ONCE port
old="""CREATE TABLE ajaxctmp AS
    SELECT cast('a' as char(1)) as type, artist.id as id ,artist.counter as counter FROM artist
    UNION
    SELECT cast('g' as char(1)) as type, artist_gallery.id as id ,artist_gallery.counter as counter FROM artist_gallery
    UNION
    SELECT cast('p' as char(1)) as type, artist_pic.id as id ,artist_pic.counter as counter FROM artist_pic;"""

#ajaxctmp contains all the count info
#initialize
#we copy ajaxctmp into ajaxctmp_work
#we append the log file info into ajaxctmp_work
#we transform ajaxctmp_work into aggregated ajaxctmp_work_ag


import sys
import re

def parse_iostring(filein,fileout):
    p=re.compile(".*httpd: AJAXC,(.),(.*)$")
    for aline in iter(filein.readline, ''): 
        # print "%s" % sL
        # else:
        #    print 'No match'
        m = p.match(aline)
        if m:
            # print 'Match found: ', m.group()
            thetype=m.group(1)
            theid=m.group(2)
            # output="type=%s, id=%s" % (thetype,theid)
            output="%s\t%s\t1\n" % (thetype,theid)
            fileout.write(output)
            # return "%s\t%s\t1" % (thetype,theid)
    return fileout


def out_sql():
    print """
DROP TABLE ajaxctmp_work;
-- initialize
SELECT * INTO ajaxctmp_work FROM ajaxctmp;

-- put new data
COPY ajaxctmp_work (type,id,counter) FROM STDIN;
"""
    parse_stdin()
    # while (<>){
    #    s/.*httpd: AJAXC,(.),(.*)$/\1\t\2\t1/;
    #    print $_;
    #    }
    # print "\\.\n";
    
    
    print """

-- create the aggregate
DROP TABLE ajaxctmp_work_ag;
CREATE TABLE ajaxctmp_work_ag AS
SELECT 
ajaxctmp_work.type         as type,
ajaxctmp_work.id           as id,
sum(ajaxctmp_work.counter) as counter
FROM ajaxctmp_work
GROUP BY type,id;


--index the aggregate
DROP   INDEX ajaxctmp_1_work_ag_idx;
CREATE INDEX ajaxctmp_1_work_ag_idx ON ajaxctmp_work_ag(type);

DROP   INDEX ajaxctmp_2_work_ag_idx;
CREATE INDEX ajaxctmp_2_work_ag_idx ON ajaxctmp_work_ag(id);

-- move the aggregate
DROP   TABLE ajaxctmp_lost;
ALTER  TABLE ajaxctmp               RENAME TO ajaxctmp_lost;
ALTER  TABLE ajaxctmp_work_ag       RENAME TO ajaxctmp;
DROP   TABLE ajaxctmp_lost;

-- rename the indexes on the aggregate
DROP   INDEX ajaxctmp_1_idx;
ALTER  INDEX ajaxctmp_1_work_ag_idx RENAME TO ajaxctmp_1_idx;


DROP   INDEX ajaxctmp_2_idx;
ALTER  INDEX ajaxctmp_2_work_ag_idx RENAME TO ajaxctmp_2_idx;

DROP   TABLE ajaxctmp_work;

"""
    
if __name__ == "__main__":
    # parse_stdin()
    # cat 1.txt |python syslogparser.py
    
    parse_iostring(sys.stdin,sys.stdout)
