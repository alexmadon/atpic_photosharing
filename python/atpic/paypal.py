#!/usr/bin/python3
# use low level:
# http://docs.python.org/release/3.1.3/library/http.client.html
# as in:
# https://www.x.com/servlet/JiveServlet/downloadBody/2199-102-1-2509/python_nv_authentication.zip
# http://stackoverflow.com/questions/4668259/connect-website-to-paypal
# or curl?
# 
import http.client
import urllib.parse

# https://svcs.sandbox.paypal.com/AdaptivePayments/API_operation

# http.client.HTTPConnection()
host="svcs.sandbox.paypal.com"
path="/AdaptivePayments/Pay"
method="POST"

json_request=""

# IMPLICIT
# to have Atpic (sandu2_1298746349_biz@madon.net) pay (sandu1_1298746254_per@madon.net)
xml_request="""<PayRequest>
<requestEnvelope>
<errorLanguage>en_US</errorLanguage>
</requestEnvelope>
<cancelUrl xmlns="">http://exammple.com/cancelURL.htm</cancelUrl>
<actionType>PAY</actionType>
<currencyCode xmlns="">USD</currencyCode>
<feesPayer>SENDER</feesPayer>
<senderEmail>sandu2_1298746349_biz@madon.net</senderEmail>
<receiverList xmlns="">
        <receiver>
            <amount>10.10</amount>
            <email>sandu1_1298746254_per@madon.net</email>
            <primary>false</primary>
            <paymentType>SERVICE</paymentType>
</receiver>
</receiverList>
<returnUrl xmlns="">http://example.com/returnURL.htm</returnUrl>
</PayRequest>"""

# SIMPLE
# to have a random user (unkown paypal) pay atpic (sandu2_1298746349_biz@madon.net)
xml_request2="""<PayRequest>
<requestEnvelope>
<errorLanguage>en_US</errorLanguage>
</requestEnvelope>
<cancelUrl xmlns="">http://exammple.com/cancelURL.htm</cancelUrl>
<actionType>PAY</actionType>
<currencyCode xmlns="">USD</currencyCode>
<receiverList xmlns="">
        <receiver>
            <amount>9.5</amount>
            <email>sandu2_1298746349_biz@madon.net</email>
            <primary>false</primary>
            <paymentType>SERVICE</paymentType>
        </receiver>
</receiverList>
<returnUrl xmlns="">http://atpic.com</returnUrl>
</PayRequest>"""


# Implicit Payments
# If you are the API caller and you specify your email address in the senderEmail field,
# PayPal implicitly approves the payment without redirecting to PayPal:
#  senderEmail Sender's email address

# params = {'spam': 1, 'eggs': 2, 'bacon': 0}

# headers.put("X-PAYPAL-SECURITY-USERID", "tok261_biz_api.abc.com");
# headers.put("X-PAYPAL-SECURITY-PASSWORD","1244612379");
# headers.put("X-PAYPAL-SECURITY-SIGNATURE","lkfg9groingghb4uw5"
# headers.put("X-PAYPAL-DEVICE-IPADDRESS", "168.212.226.204");
# headers.put("X-PAYPAL-REQUEST-DATA-FORMAT", "NV");
# headers.put("X-PAYPAL-RESPONSE-DATA-FORMAT", "NV");
# headers.put("X-PAYPAL-APPLICATION-ID", "APP-80W284485P519543T");

headers = {
    # "Content-type": "application/x-www-form-urlencoded",
    # "Accept": "text/plain",
    "X-PAYPAL-SECURITY-USERID":"sandu2_1298746349_biz_api1.madon.net",
    "X-PAYPAL-SECURITY-PASSWORD":"K6NFJUH77EBU5F6L",
    "X-PAYPAL-SECURITY-SIGNATURE":"AFcWxV21C7fd0v3bYYYRCpSSRl31AEJcxZELH15HZh6RtQrnlJWF.UDv",
    "X-PAYPAL-DEVICE-IPADDRESS":"78.86.128.147",
    "X-PAYPAL-REQUEST-DATA-FORMAT":"XML",
    "X-PAYPAL-RESPONSE-DATA-FORMAT":"XML",
    "X-PAYPAL-APPLICATION-ID":"APP-80W284485P519543T", # https://www.x.com/community/ppx/testing

    }

conn=http.client.HTTPSConnection(host)
print("connection",conn)
# enc_params = urllib.parse.urlencode(params)
conn.request(method, path, xml_request, headers)
response = conn.getresponse()
print(response.status, response.reason)

# close the connection.
data = response.read()
print("DDDAAATAAA",data)
conn.close()


# DO NOT USE: atpic is a service!
# Payments for Digital Goods
# You handle payments for digital goods in the same way you handle payments for other goods
# and services, with the following exceptions:
#    To specify a payment for digital goods, you must specify DIGITALGOODS for each receiver
#    in your receiver list; specify
#    receiverList.receiver(n).paymentType=DIGITALGOODS for each receiver,
#    where n identifies the receiver, starting with 0.
#    If you specify a payment for digital goods, you cannot specify a senderEmail address or
#    include a funding constraint.
#    You must redirect the sender to the following PayPal URL to complete the payment for
#    digital goods:
#    https://paypal.com/webapps/adaptivepayment/flow/pay?paykey=....
#    https://www.sandbox.paypal.com/webapps/adaptivepayment/flow/pay?paykey=....


# Redirecting Sender for Payment Approval
#         Use the _ap-payment command redirect Julie to PayPal to log in and approve the payment:
#         https://www.paypal.com/webscr?cmd=_ap-payment&paykey=AP-91066143KX622171A
# https://www.sandbox.paypal.com/webscr?cmd=_ap-payment&paykey=AP-91066143KX622171A
# You must redirect the sender to the following PayPal URL 
# to complete the payment for digital goods:
# https://paypal.com/webapps/adaptivepayment/flow/pay?paykey=....
