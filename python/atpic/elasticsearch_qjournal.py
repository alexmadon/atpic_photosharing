#!/usr/bin/python3
import atpic.log
import atpic.queryparser
xx=atpic.log.setmod("INFO","elasticsearch_qjournal")


def forge_permission_filter(aid):
    # authenticated id an permissions
    # we will need to parse the json output and may present only watermarked
    yy=atpic.log.setname(xx,'forge_permission_filter')
    atpic.log.debug(yy,"input=",aid)
    andpermission=b'{"or" : [ {"term" : {"aid" : "'+aid+b'"}}, {"term" : {"uid" : "'+aid+b'"}} ]}' # uid or aid is the authenticated id
    atpic.log.debug(yy,"output=",)
    return andpermission


def process_one_condition(asign,atype,avalue,outqp,outqm,outfp,outfm):
    # input:
    # =========
    # a condition (asign,atype,avalue) and three lists:
    # outqp=[] # out query +
    # outqm=[] # out query -
    # outfp=[] # out filter list +
    # outfm=[] # out filter list -
    # output: 
    # =========
    # the three list modified
    yy=atpic.log.setname(xx,'process_one_condition')
    atpic.log.debug(yy,"input=",(asign,atype,avalue,outqp,outqm,outfp,outfm))
    # we typically use query filters as score is not relevant as we sort by date desc
    outf=b'{"term" : { "'+atype+b'" : "'+avalue+b'"}}'
    if asign==b'-':
        outfm.append(outf)
    else:
        outfp.append(outf)

    atpic.log.debug(yy,"output=",(outqp,outqm,outfp,outfm))
    return (outqp,outqm,outfp,outfm)

def parsed2json(parsed,aid,afrom,size):
    yy=atpic.log.setname(xx,'parsed2json')
    atpic.log.debug(yy,"input=",(parsed,aid,afrom,size))
    ajson=b''

    outqp=[] # out query +
    outqm=[] # out query -

    outfp=[] # out filter +
    outfm=[] # out filter -

    # main loop:
    for (asign,atype,avalue) in parsed:
        (outqp,outqm,outfp,outfm)=process_one_condition(asign,atype,avalue,outqp,outqm,outfp,outfm)

    # append the permissions
    permissions=forge_permission_filter(aid)
    outfp.append(permissions)

    atpic.log.debug(yy,'outqp',outqp)
    atpic.log.debug(yy,'outqm',outqm)
    atpic.log.debug(yy,'outfp',outfp)
    atpic.log.debug(yy,'outfm',outfm)
    atpic.log.debug(yy,'+++++++')
    outl=[]
    outl.append(b'"query" : {"match_all" : {}}')
    # set the "size"
    outl.append(b'"size" : '+size)
    if afrom!=b'':
        outl.append(b'"from" : '+afrom)

    # set the fields
    # outl.append(b'"fields" : '+get_fields())

    # set the "sort"
    asort=b'"sort" : [{ "datestore" : {"order" : "desc"} }],'
    outl.append(asort)

    # set the "filter"
    if len(outfp)==1 and len(outfp)==0:
        outl.append(b'"filter" : '+b', '.join(outfp)+b'')
    else:
        # general case:
        # build a new list of negations:
        outfmm=[]
        for condn in outfm:
            outfmm.append(b'{ "not" : "'+condn+b' }')
        outl.append(b'"filter" : { "and" : ['+b', '.join(outfp+outfmm)+b']}')

    ajson=b'{ '+b', '.join(outl)+b'}'

    atpic.log.debug(yy,"output=",ajson)
    return ajson

def query2json(query,aid,afrom,size):
    # should prepend the path
    yy=atpic.log.setname(xx,'query2json')
    atpic.log.debug(yy,"input=",(query,aid,afrom,size))
    parsed=atpic.queryparser.parse_first_journal(query)
    ajson=parsed2json(parsed,aid,afrom,size)
    atpic.log.debug(yy,"output=",(parsed,ajson))
    return (parsed,ajson)
    


if __name__ == "__main__":
    print("hi")
    queries=[
        b'+aid:2 -uid:2 +method:post',
        b'+path:/user/1/gallery/23'
        ]
    aid=b'1'
    afrom=b''
    size=b'10'
    for query in queries:
        ajson=query2json(query,aid,afrom,size)
