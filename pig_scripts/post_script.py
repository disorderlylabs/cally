#!/usr/bin/python

import requests, socket

# Proxy authentication is in .conf file
f1 = open('.conf', 'r')
user = f1.readline().strip()
pwd = f1.readline().strip()
user_pass = user + ':' + pwd

# Resolve proxy to IP address.
# IP address needs to provided in 'proxs'
proxy_ip = socket.gethostbyname('c2syubi.vip.ebay.com')
proxs = {
        'https': 'https://' + str(user_pass) + '@' + str(proxy_ip) + ':443',
        'http': 'http://' + str(user_pass) + '@' + str(proxy_ip) + ':8080'
        }

s = requests.Session()
s.proxies = proxs

# Delete script. Iy either does not exist or is deleted
r = s.delete('http://appmon.vip.ebay.com/pig/script/test.pig', proxies=proxs)
assert( r.status_code in [200, 404] )

# Upload script and check that it is successful
custom_headers = {'Content-Type': 'application/octet-stream'}
fnames = {'file': open('test.pig', 'rb')}
r = s.post('http://appmon.vip.ebay.com/pig/script/test.pig', files=fnames, headers=custom_headers, proxies=proxs)
assert( r.status_code in [200, 201] )
