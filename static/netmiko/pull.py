#!/usr/bin/python3
# -*- coding: UTF-8 -*-
print('Content-Type: text/html; charset=utf-8\n')
from netmiko import ConnectHandler
import json
import cgi,cgitb
form = cgi.FieldStorage()
#usern = 'netvis'
#passw = 'ASDfgh430$'
usern = form.getvalue('username')
passw = form.getvalue('password')

print ("PROCESSING!!  Close tab if you do not see Success below......")
print("<hr/>")
my_device = {
    'host': "192.168.1.100",
    'username': usern,
    'password': passw,
    'device_type':'cisco_nxos',
}
connect = ConnectHandler(**my_device)
out1 = connect.send_command("show version | json-pretty")
f1 = open('out1.json','w')
f1.write(out1)
f1.close()
print("<hr/>")
print ("<h2>Success!! Please close the tab</h2>")

