#!/usr/bin/python3
# ctyps wrapper to libyajl
# inspired by:
# http://pykler.github.com/yajl-py/
# libyajl2 - Yet Another JSON Library

# why?
# =========
# because i do not want to decode encode /decode encode
# because It could convert directly to XML

from atpic.jsonat_include import *


# implement the callbacks:

def mynull(ctx):
    print('mynull',ctx)
    return 1
def myboolean(ctx, boolVal):
    print('myboolean',ctx, boolVal)
    return 1
def myinteger(ctx, integerVal):
    print('myinteger',ctx, integerVal)
    return 1
def mydouble(ctx, doubleVal):
    print('mydouble',ctx, doubleVal)
    return 1
def mynumber(ctx, stringVal, stringLen):
    print('mynumber',ctx, stringVal, stringLen)
    print(string_at(stringVal, stringLen))
    return 1
def mystring(ctx, stringVal, stringLen):
    print('mystring',ctx, stringVal, stringLen) # use ctypes string_at
    print(string_at(stringVal, stringLen))
    return 1
def mystart_map(ctx):
    print('mystart_map',ctx)
    return 1
def mymap_key(ctx, stringVal, stringLen):
    print('mymap_key',ctx, stringVal, stringLen)
    print(string_at(stringVal, stringLen))
    return 1
def myend_map(ctx):
    print('myend_map',ctx)
    return 1
def mystart_array(ctx):
    print('mystart_array',ctx)
    return 1
def myend_array(ctx):
    print('myend_array',ctx)
    return 1

# 
yajl_callbks = yajl_callbacks() # create a structure

# implement some prototypes
yajl_callbks.yajl_null=YAJL_NULL(mynull)
yajl_callbks.yajl_boolean=YAJL_BOOL(myboolean)
yajl_callbks.yajl_integer=YAJL_INT(myinteger)
yajl_callbks.yajl_double=YAJL_DBL(mydouble)
# yajl_callbks.yajl_number=YAJL_NUM(mynumber)
yajl_callbks.yajl_string=YAJL_STR(mystring)
yajl_callbks.yajl_start_map=YAJL_SDCT(mystart_map)
yajl_callbks.yajl_map_key=YAJL_DCTK(mymap_key)
yajl_callbks.yajl_end_map=YAJL_EDCT(myend_map)
yajl_callbks.yajl_start_array=YAJL_SARR(mystart_array)
yajl_callbks.yajl_end_array=YAJL_EARR(myend_array)

# print(yajl_callbks)
# print(yajl_callbks.yajl_end_array)

hand = yajl.yajl_alloc(byref(yajl_callbks),None,None)

print(hand)
fileData=b'{"alex" : "madon", "inside" : {"in" : "out"} }'
fileData=b'{"took":8,"timed_out":false,"_shards":{"total":1,"successful":1,"failed":0},"hits":{"total":420,"max_score":2.496926,"hits":[{"_index":"atpic","_type":"pic","_id":"2522728","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2522728",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2011-07-31T16:02:28.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-40",\n"make" : "NIKON CORPORATION",\n"focallength" : "300/10",\n"model" : "NIKON D40",\n"exposuretime" : "-66",\n"rand_0" : "-18574",\n"rand_1" : "1805",\n"rand_2" : "-12886",\n"rand_3" : "-24010",\n"rand_4" : "15693",\n"rand_5" : "-845",\n"rand_6" : "-24901",\n"rand_7" : "-26798",\n"rand_8" : "-8400",\n"rand_9" : "9171",\n"rand_10" : "-28422",\n"rand_11" : "22985",\n"rand_12" : "27670",\n"rand_13" : "14992",\n"rand_14" : "-14151",\n"rand_15" : "7973",\n"rand_16" : "15367",\n"rand_17" : "17211",\n"rand_18" : "-29267",\n"rand_19" : "-20593",\n"originalname" : "DSC_0738.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2523115","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2523115",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2012-03-25T19:25:24.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-36",\n"make" : "NIKON CORPORATION",\n"focallength" : "320/10",\n"model" : "NIKON D40",\n"exposuretime" : "-34",\n"rand_0" : "-13705",\n"rand_1" : "-8060",\n"rand_2" : "-32262",\n"rand_3" : "-27425",\n"rand_4" : "11501",\n"rand_5" : "16719",\n"rand_6" : "-4222",\n"rand_7" : "9328",\n"rand_8" : "-17006",\n"rand_9" : "-23658",\n"rand_10" : "-6909",\n"rand_11" : "29865",\n"rand_12" : "5624",\n"rand_13" : "-31535",\n"rand_14" : "-16685",\n"rand_15" : "3289",\n"rand_16" : "-11457",\n"rand_17" : "18588",\n"rand_18" : "-8968",\n"rand_19" : "-13980",\n"originalname" : "DSC_1326.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2523116","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2523116",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2012-03-25T19:25:27.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-36",\n"make" : "NIKON CORPORATION",\n"focallength" : "320/10",\n"model" : "NIKON D40",\n"exposuretime" : "-34",\n"rand_0" : "-18162",\n"rand_1" : "-19614",\n"rand_2" : "-7290",\n"rand_3" : "22630",\n"rand_4" : "-26317",\n"rand_5" : "31253",\n"rand_6" : "25967",\n"rand_7" : "-30470",\n"rand_8" : "-28935",\n"rand_9" : "-29212",\n"rand_10" : "-31268",\n"rand_11" : "-7789",\n"rand_12" : "-27539",\n"rand_13" : "16605",\n"rand_14" : "14811",\n"rand_15" : "7211",\n"rand_16" : "-11113",\n"rand_17" : "-30096",\n"rand_18" : "28843",\n"rand_19" : "-19654",\n"originalname" : "DSC_1327.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2522729","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2522729",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2011-07-31T16:02:35.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-36",\n"make" : "NIKON CORPORATION",\n"focallength" : "310/10",\n"model" : "NIKON D40",\n"exposuretime" : "-62",\n"rand_0" : "20405",\n"rand_1" : "5928",\n"rand_2" : "-10524",\n"rand_3" : "18971",\n"rand_4" : "6351",\n"rand_5" : "30555",\n"rand_6" : "15163",\n"rand_7" : "-8256",\n"rand_8" : "-14368",\n"rand_9" : "5398",\n"rand_10" : "24876",\n"rand_11" : "23187",\n"rand_12" : "22118",\n"rand_13" : "-8380",\n"rand_14" : "20430",\n"rand_15" : "3632",\n"rand_16" : "23687",\n"rand_17" : "17039",\n"rand_18" : "31660",\n"rand_19" : "12826",\n"originalname" : "DSC_0739.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2522730","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2522730",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2011-07-31T16:02:52.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "0",\n"make" : "NIKON CORPORATION",\n"focallength" : "460/10",\n"model" : "NIKON D40",\n"exposuretime" : "-58",\n"rand_0" : "5654",\n"rand_1" : "-10295",\n"rand_2" : "28732",\n"rand_3" : "-170",\n"rand_4" : "-2521",\n"rand_5" : "-1632",\n"rand_6" : "18030",\n"rand_7" : "611",\n"rand_8" : "-29637",\n"rand_9" : "17879",\n"rand_10" : "-9135",\n"rand_11" : "-25735",\n"rand_12" : "-32563",\n"rand_13" : "-11824",\n"rand_14" : "28474",\n"rand_15" : "13217",\n"rand_16" : "15143",\n"rand_17" : "-26060",\n"rand_18" : "13153",\n"rand_19" : "-32101",\n"originalname" : "DSC_0740.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2523117","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2523117",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2012-03-25T19:25:28.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-36",\n"make" : "NIKON CORPORATION",\n"focallength" : "320/10",\n"model" : "NIKON D40",\n"exposuretime" : "-34",\n"rand_0" : "-19458",\n"rand_1" : "-31013",\n"rand_2" : "6560",\n"rand_3" : "-12197",\n"rand_4" : "6011",\n"rand_5" : "-10417",\n"rand_6" : "23937",\n"rand_7" : "-32414",\n"rand_8" : "-25532",\n"rand_9" : "15545",\n"rand_10" : "7834",\n"rand_11" : "30738",\n"rand_12" : "-10547",\n"rand_13" : "-14504",\n"rand_14" : "-25458",\n"rand_15" : "-17676",\n"rand_16" : "-2948",\n"rand_17" : "-4756",\n"rand_18" : "25761",\n"rand_19" : "-3587",\n"originalname" : "DSC_1328.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2523118","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2523118",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2012-03-25T19:25:32.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-29",\n"make" : "NIKON CORPORATION",\n"focallength" : "380/10",\n"model" : "NIKON D40",\n"exposuretime" : "-34",\n"rand_0" : "409",\n"rand_1" : "14904",\n"rand_2" : "-11330",\n"rand_3" : "-14964",\n"rand_4" : "-13611",\n"rand_5" : "9931",\n"rand_6" : "-16368",\n"rand_7" : "17612",\n"rand_8" : "4736",\n"rand_9" : "14690",\n"rand_10" : "-2835",\n"rand_11" : "-25474",\n"rand_12" : "-11809",\n"rand_13" : "-9039",\n"rand_14" : "30323",\n"rand_15" : "6733",\n"rand_16" : "-28095",\n"rand_17" : "8144",\n"rand_18" : "-28813",\n"rand_19" : "-3152",\n"originalname" : "DSC_1330.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2522731","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2522731",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2011-07-31T16:05:29.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-22",\n"make" : "NIKON CORPORATION",\n"focallength" : "550/10",\n"model" : "NIKON D40",\n"exposuretime" : "-27",\n"rand_0" : "31109",\n"rand_1" : "-20371",\n"rand_2" : "13652",\n"rand_3" : "9601",\n"rand_4" : "-2765",\n"rand_5" : "-8475",\n"rand_6" : "-19808",\n"rand_7" : "-22026",\n"rand_8" : "-5801",\n"rand_9" : "-24145",\n"rand_10" : "23127",\n"rand_11" : "7163",\n"rand_12" : "11047",\n"rand_13" : "-5108",\n"rand_14" : "18214",\n"rand_15" : "29883",\n"rand_16" : "-7607",\n"rand_17" : "12135",\n"rand_18" : "-21118",\n"rand_19" : "22292",\n"originalname" : "DSC_0741.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2523119","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2523119",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2012-03-25T19:25:34.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-36",\n"make" : "NIKON CORPORATION",\n"focallength" : "310/10",\n"model" : "NIKON D40",\n"exposuretime" : "-34",\n"rand_0" : "5705",\n"rand_1" : "23826",\n"rand_2" : "-18394",\n"rand_3" : "11784",\n"rand_4" : "15776",\n"rand_5" : "-26873",\n"rand_6" : "8697",\n"rand_7" : "15222",\n"rand_8" : "2824",\n"rand_9" : "27326",\n"rand_10" : "-24079",\n"rand_11" : "13964",\n"rand_12" : "-18808",\n"rand_13" : "18779",\n"rand_14" : "20978",\n"rand_15" : "6105",\n"rand_16" : "399",\n"rand_17" : "16642",\n"rand_18" : "-12722",\n"rand_19" : "10826",\n"originalname" : "DSC_1331.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}},{"_index":"atpic","_type":"pic","_id":"2522732","_score":2.496926, "_source" : {\n"uid" : "1",\n"gid" : "49724",\n"pid" : "2522732",\n"username" : "Alex M",\n"servershort" : "alex",\n"popularity" : "0.000000000000000000000000000000",\n"price" : "0.000000000000000000000000000000",\n"mode" : "v",\n"friends" : ["2","3"],\n"tags" : [],\n"phrases" : ["nikond40"],\n"gtitle" : "nikond40",\n"ptitle" : "",\n"datetime" : "2011-07-31T16:05:36.000000Z",\n"mimetype" : "",\n"mimesubtype" : "",\n"aperture" : "-22",\n"make" : "NIKON CORPORATION",\n"focallength" : "550/10",\n"model" : "NIKON D40",\n"exposuretime" : "-51",\n"rand_0" : "-30368",\n"rand_1" : "-718",\n"rand_2" : "-5807",\n"rand_3" : "-24991",\n"rand_4" : "10149",\n"rand_5" : "18260",\n"rand_6" : "8443",\n"rand_7" : "-3341",\n"rand_8" : "-4418",\n"rand_9" : "-13762",\n"rand_10" : "24895",\n"rand_11" : "-5821",\n"rand_12" : "4862",\n"rand_13" : "-5450",\n"rand_14" : "-26564",\n"rand_15" : "-387",\n"rand_16" : "9533",\n"rand_17" : "16410",\n"rand_18" : "-9356",\n"rand_19" : "20205",\n"originalname" : "DSC_0742.JPG",\n"gpath" : "nikond40",\n"dir_0" : "/nikond40"\n}}]}}'

stat=yajl.yajl_parse(hand, fileData, len(fileData))
print('stat',stat)
print(yajl_status_ok.value)
if stat != yajl_status_ok.value:
    yajl.yajl_get_error.restype = c_char_p
    error = yajl.yajl_get_error(hand, 1, fileData, len(fileData))
    print('error:',error.decode('utf8'))
# need to clean even if there are exception
yajl.yajl_free(hand)

if __name__ == "__main__":
    print("testing json")
    
