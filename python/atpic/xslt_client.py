#!/usr/bin/python3
import zmq
# import logging
import atpic.log


xx=atpic.log.setmod("INFO","xslt_client")



def send(xml_bytes):
    """
    Sends a XML in bytes and gets the tyransformation.
    """
    yy=atpic.log.setname(xx,"send")
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://127.0.0.1:5455")
    atpic.log.debug(yy,'sending')
    socket.send(xml_bytes)
    rec=socket.recv()
    atpic.log.debug(yy,'received!')
    socket.close()
    atpic.log.debug(yy,'rec=',rec)
    return rec

if __name__ == "__main__":
    # logging.basicConfig(level=logging.DEBUG)
    xml_bytes=b"""<ok><get><get><data><user url="http://atpic.faa/user/1"><rows>0</rows><synced></synced><css>1</css><lang>fr</lang><login>alexmadon</login><usage></usage><template>0</template><id>1</id><datelast></datelast><thestyleid>1</thestyleid><size_allowed></size_allowed><storeto></storeto><servername>user6.atpic.com</servername><email>alex@madon.net</email><servershort>alex</servershort><serverip>46.4.24.136</serverip><cols>0</cols><text>a &amp;b</text><password>8dLUMa3V9.896</password><title></title><counter>15396</counter><mount>/hdc1</mount><storefrom>12</storefrom><datefirst></datefirst><name>Alex M</name></user></data></get></get></ok>"""

    rec=send(xml_bytes)
    print("Rec is:",rec)
