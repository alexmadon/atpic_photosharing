"""
This is a simple class that stores in memory the data necessary to create the 

(status,headers,output)

WSGI *response*.
It stores the response only.
Eg. the headers for the response not sent by the client in the HTTP request.
(Those are kept in the environ wsgi dictionnary.)

The reason to use an object is that we have cases where a paramter is set far in 
the processing:

e.g: 
1) set the session cookie in the XML auth level
2) the format of the output is needed to do the XSL transform and then 
later to set the content-type header. Passing those parameters around 
is tedious.

Also, we could modify the underlying storing structures in this class leaving the code more unchanged (maybe? ;) )
"""
# import logging
import atpic.log
import wsgiref.headers

class Wso():
    """
    This is a WSGI object which basically contains the status, header and output
    """
    
    def __init__(self):
        self.headersw=wsgiref.headers.Headers([]) # create a headers object
        self.output=''
        self.statuslist=[]


    def add_cookie(self,name,value):
        """
        Used to store the session just after login.
        Used to store preferences (lang, format)
        """
        pass

    def add_header(self,name,value):
        pass


    def set_format(self,environ):
        """
        Sets the target format from the WSGI environ dictionnary.
        This is used 
        1) to forge the XSL style
        2) to set the content type header
        This should use the mobile wurfl db.
        """
        pass




    def to_wsgi(self):
        # you have 3 types: file-like StringIO, string and bytes
        # wsgi expects UTF8 encoded bytes, 
        # but we try to always work with py3k strings
        status='200 ok'
        output=self.output.encode("utf-8")
        print("endtype2",type(output))
        
        headers=self.headersw.items() # transforsm a wsgiref headers object into a plain list suitable to transmit to mod_wsgi


        return (status,headers,output)

