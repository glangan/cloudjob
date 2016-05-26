#!/usr/bin/python
import cgi, os
import cgitb; cgitb.enable()
import socket
import sys
DIR = '/var/www/html/data'
cgitb.enable(display=0, logdir=DIR + '/logs')
form = cgi.FieldStorage()
# A nested FieldStorage instance holds the file
fileitem = form['file']
priority = form['priority']
# Test if the file was uploaded
if fileitem.filename:
   # strip leading path from file name to avoid directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   open('/var/www/html/data/' + fn, 'wb').write(fileitem.file.read())
   message = 'The file "' + fn + '" was uploaded successfully'
else:
   message = 'No file was uploaded'
print """\
Content-Type: text/html\n
<html><body>
<p>%s</p>
""" % (message,)
priority_value = priority.value
message = priority_value + fn


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#sock.bind(("localhost", 0))
sock.connect(("10.240.105.92", 11000))
print """\
<p> connection established </p>
"""
status_data = 'Something went wrong, please try again later'
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
print """\
<p>%s<p>
<button><a href = "http://107.167.188.250">Go Back</a></button>
</body></html>
""" % (status_data,)
