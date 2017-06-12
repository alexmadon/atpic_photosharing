# CAS for atpic
# check by service (the host name
# also check if DMS of host point to atpic.com
# do not put account mamanement under pdns.com
# put a limit on time on the serviceticket
# but still : subdomain cookie atack
# but more difficult as would have to make him click on a sub domnain...
# not too difficult
# http://code.google.com/p/browsersec/wiki/Part2
# no ability to restrict cookies to a specific host or protocol
# encode the client IP into the cookie???


# cookie scope: Scope: by default, cookie scope is limited to all URLs on the current host name - and not bound to port or protocol information. Scope may be limited with path= parameter to specify a specific path prefix to which the cookie should be sent, or broadened to a group of DNS names, rather than single host only, with domain=. The latter operation may specify any fully-qualified right-hand segment of the current host name, up to one level below TLD (in other words, www.foo.bar.example.com may set a cookie to be sent to *.bar.example.com or *.example.com, but not to *.something.else.example.com or *.com); the former can be set with no specific security checks, and uses just a dumb left-hand substring match.

# http://docs.oracle.com/cd/E19575-01/820-3320/ghtzx/index.html
# Chapter 22 Taking Precautions Against Session-Cookie Hijacking in an OpenSSO Enterprise Deployment

# http://openam.forgerock.org/openam-documentation/openam-doc-source/doc/admin-guide/index/chap-cdsso.html
# Cookie hijacking protection restricts cookies to the fully-qualified domain name (FQDN) of the host where they are issued, such as openam-server.example.com
# CDSSO stands for Cross Domain Single Sign On
# Remove the domain such as .example.com from the Cookies Domains list, and replace it with the server host name such as openam.example.com, or if OpenAM is behind a load balancer with the load balancer host name, such as load-balancer.example.com.

# http://php.net/manual/en/function.setcookie.php
# If you want to restrict the cookie to a single host, supply the domain parameter as an empty string, for example (note the rightmost parameter):
