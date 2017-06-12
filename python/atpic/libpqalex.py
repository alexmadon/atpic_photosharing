#!/usr/bin/python3
"""ctypes interface to the libpq library"""
import threading
import time
import traceback
# CODE TAKEN FROM psycopg2ct
# https://raw.github.com/mvantellingen/psycopg2-ctypes/develop/psycopg2ct/libpq.py

# see pypq python ctypes
import select
import socket


from ctypes import *
from ctypes.util import find_library
# import logging
from atpic.mybytes import *

import atpic.getconfig
import atpic.log
xx=atpic.log.setmod("INFO","libpqalex")





PG_LIBRARY = find_library('pq')
if not PG_LIBRARY:
    raise OSError('Cannot find libpq in the system')


libpq = cdll.LoadLibrary(PG_LIBRARY)
# c = libpq


c_char_p_p = POINTER(c_char_p)
c_int_p = POINTER(c_int)
c_uint_p = POINTER(c_uint)

class PGconn(Structure):
    _fields_ = []

PGconn_p = POINTER(PGconn)


class PGresult(Structure):
    _fields_ = []

PGresult_p = POINTER(PGresult)

class PGcancel(Structure):
    _fields_ = []

PGcancel_p = POINTER(PGcancel)


CONNECTION_OK = 0
CONNECTION_BAD = 1

ConnStatusType = c_int

PGRES_EMPTY_QUERY = 0
PGRES_COMMAND_OK = 1
PGRES_TUPLES_OK = 2
PGRES_COPY_OUT = 3
PGRES_COPY_IN = 4
PGRES_BAD_RESPONSE = 5
PGRES_NONFATAL_ERROR = 6
PGRES_FATAL_ERROR = 7

ExecStatusType = c_int

PG_DIAG_SEVERITY = ord('S')
PG_DIAG_SQLSTATE = ord('C')
PG_DIAG_MESSAGE_PRIMARY = ord('M')
PG_DIAG_MESSAGE_DETAIL = ord('D')
PG_DIAG_MESSAGE_HINT = ord('H')
PG_DIAG_STATEMENT_POSITION = 'P'
PG_DIAG_INTERNAL_POSITION = 'p'
PG_DIAG_INTERNAL_QUERY = ord('q')
PG_DIAG_CONTEXT = ord('W')
PG_DIAG_SOURCE_FILE = ord('F')
DIAG_SOURCE_LINE = ord('L')
PG_DIAG_SOURCE_FUNCTION = ord('R')


class PGnotify(Structure):
    pass


# Database connection control functions

PQconnectdb = libpq.PQconnectdb
PQconnectdb.argtypes = [c_char_p]
PQconnectdb.restype = PGconn_p

PQfinish = libpq.PQfinish
PQfinish.argtypes = [PGconn_p]
PQfinish.restype = None

# Connection status functions

PQdb = libpq.PQdb
PQdb.argtypes = [PGconn_p]
PQdb.restype = c_char_p

PQuser = libpq.PQuser
PQuser.argtypes = [PGconn_p]
PQuser.restype = c_char_p

PQport = libpq.PQport
PQport.argtypes = [PGconn_p]
PQport.restype = c_char_p

PQhost = libpq.PQhost
PQhost.argtypes = [PGconn_p]
PQhost.restype = c_char_p

PQstatus = libpq.PQstatus
PQstatus.argtypes = [PGconn_p]
PQstatus.restype = ConnStatusType

PQtransactionStatus = libpq.PQtransactionStatus
PQtransactionStatus.argtypes = [PGconn_p]
PQtransactionStatus.restype = c_int

PQparameterStatus = libpq.PQparameterStatus
PQparameterStatus.argtypes = [PGconn_p, c_char_p]
PQparameterStatus.restype = c_char_p

PQprotocolVersion = libpq.PQprotocolVersion
PQprotocolVersion.argtypes = [PGconn_p]
PQprotocolVersion.restype = c_int

PQserverVersion = libpq.PQserverVersion
PQserverVersion.argtypes = [PGconn_p]
PQserverVersion.restype = c_int

PQerrorMessage = libpq.PQerrorMessage
PQerrorMessage.argtypes = [PGconn_p]
PQerrorMessage.restype = c_char_p

PQbackendPID = libpq.PQbackendPID
PQbackendPID.argtypes = [PGconn_p]
PQbackendPID.restype = c_int

# Command execution functions

PQexec = libpq.PQexec
PQexec.argtypes = [PGconn_p, c_char_p]
PQexec.restype = PGresult_p

PQexecParams = libpq.PQexecParams
PQexecParams.argtypes = [PGconn_p, c_char_p, c_int, c_uint_p, c_char_p_p,
    c_int_p, c_int_p, c_int]
PQexecParams.restype = PGresult_p

PQclientEncoding = libpq.PQclientEncoding
PQclientEncoding.argtypes = [PGconn_p]
PQclientEncoding.restype = c_int

PQsetClientEncoding = libpq.PQsetClientEncoding
PQsetClientEncoding.argtypes = [PGconn_p, c_char_p]
PQsetClientEncoding.restype = c_int

pg_encoding_to_char = libpq.pg_encoding_to_char
pg_encoding_to_char.argtypes = [c_int]
pg_encoding_to_char.restype = c_char_p

PQresultStatus = libpq.PQresultStatus
PQresultStatus.argtypes = [PGresult_p]
PQresultStatus.restype = ExecStatusType

PQresultErrorMessage = libpq.PQresultErrorMessage
PQresultErrorMessage.argtypes = [PGresult_p]
PQresultErrorMessage.restype = c_char_p

PQresultErrorField = libpq.PQresultErrorField
PQresultErrorField.argtypes = [PGresult_p, c_int]
PQresultErrorField.restype = c_char_p

PQclear = libpq.PQclear
PQclear.argtypes = [POINTER(PGresult)]
PQclear.restype = None

# Retrieving query result information

PQntuples = libpq.PQntuples
PQntuples.argtypes = [PGresult_p]
PQntuples.restype = c_int

PQnfields = libpq.PQnfields
PQnfields.argtypes = [PGresult_p]
PQnfields.restype = c_int

PQfname = libpq.PQfname
PQfname.argtypes = [PGresult_p, c_int]
PQfname.restype = c_char_p

PQftype = libpq.PQftype
PQftype.argtypes = [PGresult_p, c_int]
PQftype.restype = c_uint

PQgetisnull = libpq.PQgetisnull
PQgetisnull.argtypes = [PGresult_p, c_int, c_int]
PQgetisnull.restype = c_int

PQgetlength = libpq.PQgetlength
PQgetlength.argtypes = [PGresult_p, c_int, c_int]
PQgetlength.restype = c_int

PQgetvalue = libpq.PQgetvalue
PQgetvalue.argtypes = [PGresult_p, c_int, c_int]
PQgetvalue.restype = c_char_p

# Retrieving other result information

PQcmdStatus = libpq.PQcmdStatus
PQcmdStatus.argtypes = [PGresult_p]
PQcmdStatus.restype = c_char_p

PQcmdTuples = libpq.PQcmdTuples
PQcmdTuples.argtypes = [PGresult_p]
PQcmdTuples.restype = c_char_p

PQoidValue = libpq.PQoidValue
PQoidValue.argtypes = [PGresult_p]
PQoidValue.restype = c_uint

# Escaping string for inclusion in sql commands

#if PG_VERSION >= 0x090000:
#    PQescapeLiteral = libpq.PQescapeLiteral
#    PQescapeLiteral.argtypes = [PGconn_p, c_char_p, c_uint]
#    PQescapeLiteral.restype = POINTER(c_char)

PQescapeStringConn = libpq.PQescapeStringConn
PQescapeStringConn.restype = c_uint
PQescapeStringConn.argtypes = [PGconn_p, c_char_p, c_char_p, c_uint, POINTER(c_int)]

PQescapeString = libpq.PQescapeString
PQescapeString.argtypes = [c_char_p, c_char_p, c_uint]
PQescapeString.restype = c_uint

PQescapeByteaConn = libpq.PQescapeByteaConn
PQescapeByteaConn.argtypes = [PGconn_p, c_char_p, c_uint, POINTER(c_uint)]
PQescapeByteaConn.restype = POINTER(c_char)

PQescapeBytea = libpq.PQescapeBytea
PQescapeBytea.argtypes = [c_char_p, c_uint, POINTER(c_uint)]
PQescapeBytea.restype = POINTER(c_char)

PQunescapeBytea = libpq.PQunescapeBytea
PQunescapeBytea.argtypes = [POINTER(c_char), POINTER(c_uint)]
PQunescapeBytea.restype = POINTER(c_char)

# Cancelling queries in progress

PQgetCancel = libpq.PQgetCancel
PQgetCancel.argtypes = [PGconn_p]
PQgetCancel.restype = PGcancel_p

PQfreeCancel = libpq.PQfreeCancel
PQfreeCancel.argtypes = [PGcancel_p]
PQfreeCancel.restype = None

PQcancel = libpq.PQcancel
PQcancel.argtypes = [PGcancel_p, c_char_p, c_int]
PQcancel.restype = c_int

PQrequestCancel = libpq.PQrequestCancel
PQrequestCancel.argtypes = [PGconn_p]
PQrequestCancel.restype = c_int

# Miscellaneous functions

PQfreemem = libpq.PQfreemem
PQfreemem.argtypes = [c_void_p]
PQfreemem.restype = None

# Notice processing

PQnoticeProcessor = CFUNCTYPE(None, c_void_p, c_char_p)

PQsetNoticeProcessor = libpq.PQsetNoticeProcessor
PQsetNoticeProcessor.argtypes = [PGconn_p, PQnoticeProcessor, c_void_p]
PQsetNoticeProcessor.restype = PQnoticeProcessor







#
# ALEX
#
#

PQprepare = libpq.PQprepare
PQprepare.argtypes = [PGconn_p, c_char_p, c_char_p, c_int, c_uint_p]
PQprepare.restype = PGresult_p


PQexecPrepared = libpq.PQexecPrepared
PQexecPrepared.argtypes = [PGconn_p, c_char_p, c_int, c_char_p_p,
    c_int_p, c_int_p, c_int]
PQexecPrepared.restype = PGresult_p


# alex async
PQsendQueryParams = libpq.PQsendQueryParams
PQsendQueryParams.restype = c_int
PQsendQueryParams.argtypes =  [PGconn_p, c_char_p, c_int, c_uint_p, c_char_p_p,
    c_int_p, c_int_p, c_int]


PQsendPrepare = libpq.PQsendPrepare
PQsendPrepare.argtypes = [PGconn_p, c_char_p, c_char_p, c_int, c_uint_p]
PQsendPrepare.restype = c_int


PQsendQueryPrepared = libpq.PQsendQueryPrepared
PQsendQueryPrepared.argtypes =  [PGconn_p, c_char_p, c_int, c_char_p_p,
    c_int_p, c_int_p, c_int]
PQsendQueryPrepared.restype = c_int


PQgetResult = libpq.PQgetResult
PQgetResult.restype = PGresult_p
PQgetResult.argtypes = [PGconn_p]

PQconsumeInput = libpq.PQconsumeInput
PQconsumeInput.restype = c_int
PQconsumeInput.argtypes = [PGconn_p]


PQisBusy = libpq.PQisBusy
PQisBusy.restype = c_int
PQisBusy.argtypes = [PGconn_p]

PQsetnonblocking = libpq.PQsetnonblocking
PQsetnonblocking.restype = c_int
PQsetnonblocking.argtypes = [PGconn_p, c_int]

PQisnonblocking = libpq.PQisnonblocking
PQisnonblocking.restype = c_int
PQisnonblocking.argtypes = [PGconn_p]

PQflush = libpq.PQflush
PQflush.restype = c_int
PQflush.argtypes = [PGconn_p]

PQsocket = libpq.PQsocket
PQsocket.restype = c_int
PQsocket.argtypes = [PGconn_p]

# ###########################################
#           low level wrappers
# ###########################################


# low level mapping to libpq start with pq_ 
# (replace the upper case with _ lower case)
# we simplify the syntax by removing arguments in the function
# when this is possible

# connection functions
def pq_socket(conn):
    socket_nb=libpq.PQsocket(conn)
    return socket_nb

def pq_port(conn):
    port=libpq.PQport(conn)
    return port

def pq_connect_db(connstr):
    conn=libpq.PQconnectdb(connstr)
    return conn

def pq_finish(conn):
    PQfinish(conn)

def pq_socket(conn):
    return PQsocket(conn)

# error functions
def pq_result_error_message(res):
    return PQresultErrorMessage(res)
# execution functions 

def pq_exec(conn, query):
    result = libpq.PQexec(conn, query)
    return result

def pq_exec_params(conn,query,values):
    n_args = len(values)
    lengths=map(len,values)
    formats=map(zero,values)

    # Create c types for parameter arrays
    arr_chars_t = c_char_p * n_args
    arr_ints_t = c_int * n_args
    arr_uints_t = c_uint * n_args
    result = libpq.PQexecParams(
        conn, query,
        n_args, # int nParams,
        # Passing oids only creates problems, so ignore that param
        # arr_uints_t(*types), # const Oid *paramTypes,
        None,
        arr_chars_t(*values), # const char * const *paramValues,
        arr_ints_t(*lengths), # const int *paramLengths,
        arr_ints_t(*formats), # const int *paramFormats,
        0 # int resultFormat
        )
    return result



def pq_prepare(conn,statement_name,query):
    #  we remove the last two parameters:
    # oid types: not used
    # nparams: we compute the value based on the number of $'s
    yy=atpic.log.setname(xx,'pq_prepare')
    atpic.log.debug(yy,conn,statement_name,query)
    
    nparams=statement_name.count(b'$')
    atpic.log.debug(yy,'nparams',nparams)
    result=libpq.PQprepare(conn, # PGconn *conn,
                           statement_name, # const char *stmtName,
                           query, # const char *query,
                           nparams, # int nParams,
                           None) # const Oid *paramTypes
    check_prepare_result(result)
    return result



def pq_exec_prepared(conn,statement_name,values):
    # The parameters are identical to PQexecParams, except that the name of a prepared statement is given instead of a query string, 
    # and the paramTypes[] parameter is not present 
    # (it is not needed since the prepared statement's parameter types were determined when it was created).

    yy=atpic.log.setname(xx,'pq_exec_prepared')
    atpic.log.debug(yy,conn,statement_name,values)
    n_args=len(values)
    lengths=map(len,values)
    formats=map(zero,values)

    # Create c types for parameter arrays
    arr_chars_t = c_char_p * n_args
    arr_ints_t = c_int * n_args
    arr_uints_t = c_uint * n_args

    result=libpq.PQexecPrepared(conn, # PGconn *conn,
                                statement_name, # const char *stmtName,
                                n_args, # int nParams,
                                arr_chars_t(*values), # const char * const *paramValues,
                                arr_ints_t(*lengths), # const int *paramLengths,
                                arr_ints_t(*formats), # const int *paramFormats,
                                0) # int resultFormat

    return result








# asynchronous execution functions
# http://oldmoe.blogspot.com/2008/07/faster-io-for-ruby-with-postgres.html

def pq_send_query_params(conn,query,values):
    yy=atpic.log.setname(xx,'pq_send_query_params')
    atpic.log.debug(yy,conn,query,values)
    n_args = len(values)
    lengths=map(len,values)
    formats=map(zero,values)

    # Create c types for parameter arrays
    arr_chars_t = c_char_p * n_args
    arr_ints_t = c_int * n_args
    arr_uints_t = c_uint * n_args
    result = libpq.PQsendQueryParams(
        conn, query,
        n_args, # int nParams,
        # Passing oids only creates problems, so ignore that param
        # arr_uints_t(*types), # const Oid *paramTypes,
        None,
        arr_chars_t(*values), # const char * const *paramValues,
        arr_ints_t(*lengths), # const int *paramLengths,
        arr_ints_t(*formats), # const int *paramFormats,
        0 # int resultFormat
        )
    return result



def pq_send_prepare(conn,statement_name,query):
    #  we remove the last two parameters:
    # oid types: not used
    # nparams: we compute the value based on the number of $'s
    yy=atpic.log.setname(xx,'pq_prepare')
    atpic.log.debug(yy,conn,statement_name,query)
    
    nparams=statement_name.count(b'$')
    result=libpq.PQsendPrepare(conn, # PGconn *conn,
                           statement_name, # const char *stmtName,
                           query, # const char *query,
                           nparams, # int nParams,
                           None) # const Oid *paramTypes
    return result


def pq_send_query_prepared(conn,statement_name,values):
    # The parameters are identical to PQexecParams, except that the name of a prepared statement is given instead of a query string, 
    # and the paramTypes[] parameter is not present 
    # (it is not needed since the prepared statement's parameter types were determined when it was created).

    yy=atpic.log.setname(xx,'pq_exec_prepared')
    atpic.log.debug(yy,conn,statement_name,values)
    n_args=len(values)
    lengths=map(len,values)
    formats=map(zero,values)

    # Create c types for parameter arrays
    arr_chars_t = c_char_p * n_args
    arr_ints_t = c_int * n_args
    arr_uints_t = c_uint * n_args

    result=libpq.PQsendQueryPrepared(conn, # PGconn *conn,
                                statement_name, # const char *stmtName,
                                n_args, # int nParams,
                                arr_chars_t(*values), # const char * const *paramValues,
                                arr_ints_t(*lengths), # const int *paramLengths,
                                arr_ints_t(*formats), # const int *paramFormats,
                                0) # int resultFormat

    return result

def pq_get_result(conn):
    res=PQgetResult(conn)
    return res

def pq_setnonblocking(conn,mode):
    return PQsetnonblocking(conn,mode)


def pq_is_busy(conn):
    return PQisBusy(conn)

def pq_consume_input(conn):
    return PQconsumeInput(conn)

# #################################
#      higher level
# #################################




class Fatal(Exception):
    def __init__(self,state):
        self.state=state # state is an array
        self.content=b'SQL error'

class Unexpected(Exception):
    def __init__(self,msg):
        self.msg=msg




def set_fatal(result):
    yy=atpic.log.setname(xx,'set_fatal')
    atpic.log.error(yy,'PGRES_FATAL_ERROR')
    errmsg=libpq.PQresultErrorMessage(result)
    atpic.log.error(yy,'errmsg',errmsg)
    message_primary=libpq.PQresultErrorField(result,PG_DIAG_MESSAGE_PRIMARY)
    atpic.log.error(yy,'message_primary',message_primary)
    sqlstate=libpq.PQresultErrorField(result,PG_DIAG_SQLSTATE)
    atpic.log.error(yy,'sqlstate',sqlstate) # 23505 	unique_violation
    hint=libpq.PQresultErrorField(result,PG_DIAG_MESSAGE_HINT)
    atpic.log.error(yy,'hint',hint)
    # state is an array
    if sqlstate==None:
        sqlstate=b''
    if hint==None:
        hint=b''
    if errmsg==None:
        errmsg=b''
    if message_primary==None:
        message_primary=b''
    fatalerror={b'sqlstate':sqlstate,b'hint':hint,b'msg':errmsg,b'primary':message_primary}
    atpic.log.error(yy,'output=',fatalerror)
    return fatalerror


def check_prepare_result(result):
    yy=atpic.log.setname(xx,'check_prepare_result')
    atpic.log.debug(yy,result)
    # analyse the results
    status=PQresultStatus(result)
    atpic.log.debug(yy,'status',status)
    # if status == PGRES_TUPLES_OK:
    #     atpic.log.debug(yy,'PGRES_TUPLES_OK')
    if status == PGRES_TUPLES_OK:
        atpic.log.debug(yy,'PGRES_TUPLES_OK')
    elif status == PGRES_FATAL_ERROR:
        fatalerror=set_fatal(result)
        libpq.PQclear(result)
        raise Fatal(fatalerror)
    elif status == PGRES_COMMAND_OK:
        atpic.log.debug(yy,'PGRES_COMMAND_OK')
    else:
        atpic.log.error(yy,'Unexpected prepared pgresultstatus %s',status)


def process_result(result):
    yy=atpic.log.setname(xx,'process_result')
    atpic.log.debug(yy,result)
    bigres=[]

    # analyse the results
    status=PQresultStatus(result)
    atpic.log.debug(yy,'status',status)
    if status == PGRES_TUPLES_OK:
        atpic.log.debug(yy,'PGRES_TUPLES_OK')
        rowcount = libpq.PQntuples(result)
        atpic.log.debug(yy,'rowcount',rowcount)
        rownumber = 0
        # get the fields
        nfields = libpq.PQnfields(result)
        for rownumber in range(0,rowcount):
            atpic.log.debug(yy,'row',rownumber)
            arow={}
            for i in range(0,nfields):
                fname = libpq.PQfname(result, i)
                # fname=fnames[i]
                value = libpq.PQgetvalue(result, rownumber, i)
                # print(rownumber, i, value)
                arow[fname]=value
            bigres.append(arow)
        libpq.PQclear(result)
    elif status == PGRES_FATAL_ERROR:
        fatalerror=set_fatal(result)
        libpq.PQclear(result)
        raise Fatal(fatalerror)
    elif status == PGRES_COMMAND_OK:
        atpic.log.debug(yy,'PGRES_COMMAND_OK')
        rowcount = int(libpq.PQcmdTuples(result) or -1)
        atpic.log.debug(yy,'rowcount',rowcount)
        libpq.PQclear(result)

    else:
        fatalerror=set_fatal(result)
        libpq.PQclear(result)
        raise Fatal(fatalerror)
        # libpq.PQclear(result)
        # raise Fatal('Unexpected pgresultstatus %s' % status)

    atpic.log.debug(yy,bigres)
    atpic.log.debug(yy,'cleared',result)

    return bigres










def process_result_with_callback(result,callback,*args):
    """
    Input: result is the SQL result pointer
    callback: is a function that will be called for each row
    with 'row' and *args as parameters
    """
    yy=atpic.log.setname(xx,'process_result_with_callback')
    atpic.log.debug(yy,result)


    # analyse the results
    status=PQresultStatus(result)
    atpic.log.debug(yy,'status',status)
    if status == PGRES_TUPLES_OK:
        atpic.log.debug(yy,'PGRES_TUPLES_OK')
        rowcount = libpq.PQntuples(result)
        atpic.log.debug(yy,'rowcount',rowcount)
        
        # get the fields
        nfields = libpq.PQnfields(result)
        for rownumber in range(0,rowcount):
            atpic.log.debug(yy,'row',rownumber)
            arow={}
            for i in range(0,nfields):
                fname = libpq.PQfname(result, i)
                value = libpq.PQgetvalue(result, rownumber, i)
                arow[fname]=value
            # now the callback
            try:
                callback(rownumber,arow,*args)
            except:
                atpic.log.debug(yy,'There was an error in callback')
                atpic.log.error(yy,traceback.format_exc())

                # print('There was an error in callback')
        libpq.PQclear(result)
    elif status == PGRES_FATAL_ERROR:
        fatalerror=set_fatal(result)
        libpq.PQclear(result)
        raise Fatal(fatalerror)
    elif status == PGRES_COMMAND_OK:
        atpic.log.debug(yy,'PGRES_COMMAND_OK')
        rowcount = int(libpq.PQcmdTuples(result) or -1)
        atpic.log.debug(yy,'rowcount',rowcount)
        libpq.PQclear(result)
    else:
        libpq.PQclear(result)
        raise Unexpected('Unexpected pgresultstatus %s' % status)

    atpic.log.debug(yy,'cleared',result)



def get_connstr_native():
    # connection to pg (native port 5432)
    config_array=atpic.getconfig.parse_config()
    connstr=b"hostaddr = '"+config_array["db_addr"].encode('utf8')+b"' port = '"+config_array["db_port"].encode('utf8')+b"' dbname = '"+config_array["db_name"].encode('utf8')+b"' user = '"+config_array["db_user"].encode('utf8')+b"' password = '"+config_array["db_password"].encode('utf8')+b"' connect_timeout = '10'"
    return connstr

def get_connstr_pgbouncer():
    # connection to pgbouncer (port 6432)
    config_array=atpic.getconfig.parse_config()
    connstr=b"hostaddr = '"+config_array["db_addr"].encode('utf8')+b"' port = '"+config_array["pgbouncer_port"].encode('utf8')+b"' dbname = '"+config_array["db_name"].encode('utf8')+b"' user = '"+config_array["db_user"].encode('utf8')+b"' password = '"+config_array["db_password"].encode('utf8')+b"' connect_timeout = '10'"
    return connstr

def db():
    # connection to pgbouncer (port 6432)
    connstr=get_connstr_pgbouncer()
    conn=db_connstr(connstr)
    return conn

def db_native():
    # connection to pg (native port 5432)
    connstr=get_connstr_native()
    conn=db_connstr(connstr)
    return conn


def db_connstr(connstr):
    yy=atpic.log.setname(xx,'db')
    atpic.log.debug(yy,'opening connection')
    # conn=libpq.PQconnectdb(connstr)
    conn=pq_connect_db(connstr)
    if not conn:
        atpic.log.debug(yy,"libpq error: PQconnectdb returned NULL.")
        raise Fatal("libpq error: PQconnectdb returned NULL!!!")
    if PQstatus(conn) != CONNECTION_OK:
        atpic.log.debug(yy,"libpq error: PQstatus(psql) != CONNECTION_OK")
        raise Fatal("libpq error: PQstatus(psql) != CONNECTION_OK!!!")
    return conn

def close(conn):
    yy=atpic.log.setname(xx,'close')
    atpic.log.debug(yy,'closing connection')
    pq_finish(conn)

def zero(x):
    # return a 0 for any input
    return 0
def process_send_result(res,conn):
    yy=atpic.log.setname(xx,'process_send_result')
    atpic.log.debug(yy,'res',res)
    if res==0:
        errmsg=libpq.PQerrorMessage(conn)
        # errmsg=libpq.PQresultErrorMessage(result)
        print(errmsg)
        raise Fatal
# ##########################
#          tests
# ##########################


def test_speed_connect():
    """
    tests the speed of connection without middleware, with pgpool, pgbouncer
    """
    connstr=get_connstr_pgbouncer()

    start = time.clock()
    nb=10000
    for i in range(0,nb):
        conn=libpq.PQconnectdb(connstr)
        PQfinish(conn)
    elapsed = time.clock() - start
    print(elapsed,'s, ',elapsed/nb,' s/con, ', nb/elapsed,'per sec')


def test_speed_prepare(conn):
    statement_name=b''
    #  a SELECT * is very costfull
    # query=b'select id,_user,_datetimeoriginal from _user_gallery_pic where _user=$1 and _gallery=$2 order by id limit 10'
    # query=b'select id from _user_gallery_pic where _user=$1 and _gallery=$2 order by id limit 10'

    query=b'select * from _user_gallery_pic where _user=$1 and id=$2'

    values=[b'1',b'1']
    t1=time.clock()
    max=100
    for i in range(0,max):
        prepare(conn,statement_name,query)
    t2=time.clock()
    for i in range(0,max):
        res=exec_prepared(conn,statement_name,values)
    t3=time.clock()


    for i in range(0,max):
        res=pq_exec_params(conn,query,values)
        # res=process_result(res)
        # print(res)
    t4=time.clock()

    print(t2-t1,t3-t2)
    print(t3-t1,'vs',t4-t3)
    # print(res)





def test_speed_process_result(conn):
    """
    Evaluate the cost of return an array instead of a PGresult
    """
    statement_name=b''
    #  a SELECT * is very costfull
    # query=b'select id,_user,_datetimeoriginal from _user_gallery_pic where _user=$1 and _gallery=$2 order by id limit 10'
    # query=b'select id from _user_gallery_pic where _user=$1 and _gallery=$2 order by id limit 10'

    query=b'select id from _user_gallery_pic where _user=$1 and _gallery=$2 limit 20'

    values=[b'1',b'1']
    t1=time.clock()
    max=100
    for i in range(0,max):
        prepare(conn,statement_name,query)
        result=pq_exec_params(conn,query,values)
        result=process_result(result)
        # print(result)
        alist=[]
        for row in result:
            for key in row.keys():
                # print(key,row[key])
                alist.append((key,row[key]))
    t2=time.clock()

    for i in range(0,max):
        prepare(conn,statement_name,query)
        result=pq_exec_params(conn,query,values)
        result=process_result(result)

    t3=time.clock()
    print(t2-t1,t3-t2)

def test_async():

    query_list=[
        (b'select * from _user where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery_pic where id>$1 order by id limit 20',[b'1']),
        ]

    results=async_query(query_list)

def async_query(query_list):
    yy=atpic.log.setname(xx,'async_query')

    mypid=threading.current_thread()
    # print('mypid',mypid)
    full_list=[]
    rlist=[] #  list of socket to be used by select.select()
    position=0
    for (query,values) in query_list:
        # open one socket per query
        conn=db()
        atpic.log.debug(yy,conn)
        # send the query
        res=pq_send_query_params(conn,query,values)
        # store the socket id
        sock=pq_socket(conn)
        atpic.log.debug(yy,'socket',sock)
        full_list.append([position,conn,sock,query,values])
        # whatch the read state of that socket:
        rlist.append(sock)
        position=position+1


    # print('rlist',rlist)
    # do a select
    # file:///home/madon/doc/python_3.3a0_docs_html/library/select.html
    timeout=0.1
    # rlist is defined above
    wlist=[]
    xlist=[]


    # Several things to be noted. 
    # First, one cannot process several commands using the same connection at once. 
    # You need several connections to achieve parallel command processing.
    consumed=set()
    busy=list()
    terminated=list()
    full_results=[]
    i=0
    while True:
        i=i+1
        atpic.log.debug(yy,'++++++++++++++++++++',i,'+++++++++++++++++++')
        red=select.select(rlist, wlist, xlist, 0.00001)
        atpic.log.debug(yy,red)
        print('ready',red)
        for asock in red[0]:
            atpic.log.debug(yy,'processing sock',asock)
            for [position,conn,sock,query,values] in full_list:
                if sock==asock:
                    atpic.log.debug(yy,'consume sock',sock)
                    rconsume=pq_consume_input(conn)
                    consumed.add(asock)
                    busy.append((position,conn,sock,query,values))
                    # busy.add(asock)
        atpic.log.debug(yy,'checking busy',busy)
        # need to remove an element from a list in a loop
        # http://www.daniweb.com/software-development/python/threads/73944
        for (position,conn,sock,query,values) in busy[:]:
            atpic.log.debug(yy,'AAA checking busy sock',sock)
            rbusy=pq_is_busy(conn)
            atpic.log.debug(yy,'BBBB rbusy=', rbusy,'sock',sock)
            if rbusy==1:
                atpic.log.debug(yy,'sock',sock,'is busy, we will read later')
            elif rbusy==0:
                atpic.log.debug(yy,'sock',sock,'is NOT busy, we can read now')
                result=pq_get_result(conn)
                result=process_result(result)
                terminated.append(conn)
                full_results.append((position,query,values,result))
                busy.remove((position,conn,sock,query,values))
            else:
                atpic.log.debug(yy,'sock',sock,'is unkown rbusy=',rbusy)
        
        atpic.log.debug(yy,'terminated',terminated)
        # exit the loop when done
        if len(terminated)==len(full_list):
            atpic.log.debug(yy,'we are done')
            break

    # closing the connections
    for conn in terminated:
        atpic.log.debug(yy,"closing conn",conn)
        close(conn)
    # atpic.log.debug(yy,'=====================================')
    # atpic.log.debug(yy,'full_results',full_results)
    # sort based on position

    full_results_sorted=sorted(full_results, key=lambda full_results: full_results[0]) 
    # atpic.log.debug(yy,'-------------------------------------')
    # atpic.log.debug(yy,'full_results_sorted',full_results_sorted)
    # http://stackoverflow.com/questions/3308102/how-to-extract-the-n-th-elements-from-a-list-of-tuples-in-python
    results_sorted=[x[3] for x in full_results_sorted]
    # atpic.log.debug(yy,'++++++++++++++++++++++++++++++++++++')
    # atpic.log.debug(yy,'results_sorted',results_sorted)
    return results_sorted






def test_async_wrap_SIMPLE():
    """
    Tests if you can send two requests async and get the resulst later
    """
    query_list=[
        (b'select * from _user where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery_pic where id>$1 order by id limit 20',[b'1']),
        ]
    # open just one connection
    conn=db()
    for (query,values) in query_list:
        res=pq_send_query_params(conn,query,values)
        res=process_send_result(res,conn)
        res1=pq_get_result(conn)
        PQclear(res1)
        # res=pq_exec_params(conn,query,values)
        # res=process_result(res)
        for i in range(0,10):
            print('#######',i)
            res1=pq_get_result(conn)
            PQclear(res1)
            # print('res1',res1)
            # print(bool(res1))
        # res2=process_result(res1)

def test_async_wrap():
    """
    Tests if you can send two requests async and get the resulst later
    """
    query_list=[
        (b'select * from _user where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery_pic where id>$1 order by id limit 20',[b'1']),
        ]
    # open just one connection
    conn=db()
    i=0
    for (query,values) in query_list:
        i=i+1
        statement_name=b'statement'+int2bytes(i)
        res=pq_send_prepare(conn,statement_name,query)
        print('resaaa',res)
    i=0
    for (query,values) in query_list:
        i=i+1
        statement_name=b'statement'+int2bytes(i)
        res=pq_send_query_prepared(conn,statement_name,values)
        # res=pq_send_query_params(conn,query,values)
        res=process_send_result(res,conn)
        res1=pq_get_result(conn)
        PQclear(res1)
        # res=pq_exec_params(conn,query,values)
        # res=process_result(res)
        for i in range(0,10):
            print('#######',i)
            res1=pq_get_result(conn)
            PQclear(res1)
            # print('res1',res1)
            # print(bool(res1))
        # res2=process_result(res1)






def test_openclose():
    """
    is the time to open a new connection negligible?
    """
    query_list=[
        # (b'select * from _user where id=$1 order by id limit 20',[b'1']),
        # (b'select * from _user_gallery where id>$1 order by id limit 20',[b'1']),
        (b'select * from _user_gallery_pic where id>$1 order by id limit 20',[b'1']),
        ]
    # open just one connection
    maxi=100
    t1=time.clock()
    # conn=db()
    for i in range(0,maxi):
        for (query,values) in query_list:
            # res=pq_send_query_params(conn,query,values)
            # res=process_send_result(res,conn)
            # res1=pq_get_result(conn)
            # PQclear(res1)
            conn=db()
            res=pq_exec_params(conn,query,values)
            res=process_result(res)
            close(conn)
    # close(conn)
    t2=time.clock()
    print('elapsed',t2-t1)






if __name__ == "__main__":

    # logging.basicConfig(level=logging.WARN)

    # test_speed_prepare(conn)
    # test_speed_process_result(conn)
    # test_async()
    # test_speed_connect()
    # test_async_wrap()
    test_openclose()

    # parse_config()

    """quit()

    # logging.basicConfig(level=logging.DEBUG)
    conn=db()
    conn=connect(connstr)

    print(conn)


    if not conn:
        print("libpq error: PQconnectdb returned NULL.\n\n")
    
    if PQstatus(conn) != CONNECTION_OK:
        print("libpq error: PQstatus(psql) != CONNECTION_OK\n\n")


    # send a query

    query=b"SELECT * from _user limit 2"
    result = query_exec(conn, query)
    print(result)


    # send a query with parameters
    query=b"SELECT * FROM _user WHERE id in ($1,$2)"
    
    values=[b'1',b'20']
    query=b"select * from _user where _login=$1"
    values=(b'alexmadon',)

    # result=pq_exec_params(conn,query,values)

    # a prepared statement
    statement=b"statement1"
    result1=pq_prepare(conn,statement,query)
    result=pq_exec_prepared(conn,statement,values)
    print(result)
    res=process_result(result)
    print(res)
    # print(dir(res[0]))
    PQfinish(conn)
    """
