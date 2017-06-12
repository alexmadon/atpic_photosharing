#!/usr/bin/python3
import zmq
import time
from lxml import etree
import io
# import logging
import atpic.log


xx=atpic.log.setmod("INFO","xslt_server")



def create_server():
    yy=atpic.log.setname(xx,"create_server")
    # client server like
    context=zmq.Context()
    server=context.socket(zmq.REP)
    server.bind("tcp://127.0.0.1:5455")
    xslfile="/home/madon/public_html/perso/entreprise/sql_current/site/atpic/python/atpic/all.xsl"
    xslt_doc = etree.parse(xslfile)
    transform = etree.XSLT(xslt_doc)
    return (server,transform)

def rec_send(server,transform):
    yy=atpic.log.setname(xx,"rec_send")
    message=server.recv()
    atpic.log.debug(yy,'receied',message)
    xml_string=io.BytesIO(message)
    xml_doc = etree.parse(xml_string)
    xml_doc_new = transform(xml_doc)
    atpic.log.debug(yy,'sending')
    print(time.time())
    server.send(xml_doc_new)


def main_loop(server,transform):
    yy=atpic.log.setname(xx,"main_loop")
    while True:
        rec_send(server,transform)

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    (server,transform)=create_server()
    main_loop(server,transform)

    
    



