import urllib2
import re


proxy_info = {
'username' : 'username',
'password' : 'password',
'host' : "XXX.XXX.XX.XX",
'port' : XXXX   			#not single or double quotes. 
}

# building a new opener to open the link in proxy enviorment
proxy_support = urllib2.ProxyHandler({"http" : \
"http://%(username)s:%(password)s@%(host)s:%(port)d" % proxy_info})

opener = urllib2.build_opener(proxy_support, urllib2.HTTPHandler)

# install the opener
urllib2.install_opener(opener)
