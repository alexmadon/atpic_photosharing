# Atpic Photosharing

This is the python source code of `atpic.com` (http://atpic.com) a phot sharing site that I use to test various technologies.

## Features:

* wiki where photos can easily be intserted (extended reStructuredText format)
* a virtual filesystem used to make in-place uploads by FTP possible
* search with a rich syntax
* search supports CJK and Thai
* REST API: the site itself uses it
* API data in XML or JSON
* site uses a XSLT style sheet for the presentation layer
* dns based load balancing with custom dns server
* atpic.com for the API, atpicdata.com for the content
* CSRF and antidos protection
* WURFL based device identification

## Technologies Used

* python3 with several Ctypes drivers
* elasticsearch for search
* pyparsing for search grammar
* redis
* virtualization (qemu) for the transformation layer. Look at the list of security bugs to convince you you should not run that in a non secured layer
https://www.cvedetails.com/vulnerability-list/vendor_id-1749/Imagemagick.html
* ZeroMQ for message passing
* fuse
* xslt
* openssl
* docutils

## TODO

* investigate replacing QEMU with docker containers
* need better scaling or clustering
* work on the presentation layer
* try a presentation with angular2
* work on usability
* populate the wiki with a good documentation
* document the API with swagger/OpenAPI Specification(OAS)