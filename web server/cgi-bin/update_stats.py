#!/usr/bin/python
import socket
import sys
import os
DIR = '/var/www/html/data'
print """\
Content-Type: text/html\n
<html><body>
<p>Server Stats</p>
"""
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind(("localhost", 0))
sock.connect(("10.240.105.92", 11000))
message = 'status'
status_data = 'Cannot obtain status data'
try:
        #send data
        sock.sendall(message)
        #Look for responses
        data_recv = sock.recv(1024)
finally:
        sock.close()
if data_recv:
        f = open(DIR + '/' + data_recv, 'r')
        status_data = f.read()
        f.close()
        os.remove(DIR + '/' + data_recv)
node_status = status_data.split('/')[:-1]
job_status = status_data.split('/')[-1]

for node in node_status:
        print """\
        <h3>Node Status</h3>
        <p>%s</p>
        """ % (node,)
print """
<h3>Job status</h3>
<p>%s</p>
<a href="http://107.167.188.250/">Go back</a>
</body></html>
""" % (job_status,)
