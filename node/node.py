import os, os.path
from thread import *
import socket
import sys
from time import sleep
import psutil
#set directory for file storage and retrieval
DIR = '/home/gauravlangan_gmail_com/data'
NODE_IP = '10.240.149.254'
#handle python file
def file_handle_py(file_in):
        file_out = 'output-node2' + str(client_address[1])
        os.system("python " + DIR + "/" + file_in + " >> " + DIR + "/" + file_out)   #run python file and generate output file
        return file_out
#handle c file
def file_handle_c(file_in):
        file_out = 'output-node1'
        file_name = file_in.split('.')[0]
        os.system("gcc " + DIR + "/" + file_in + ' -o ' + DIR + '/' + file_name)
        os.system("./data/" + file_name + " >> " + DIR + "/" + file_out)
        return file_out
#find and show server CPU, memory to show status to client
def show_status():
        file_out = 'status-node2'
        f = open(DIR + '/' + file_out, 'a+')
        cpu_no = str(psutil.cpu_count())
        cpu_per = str(psutil.cpu_percent())
        mem_usage = psutil.virtual_memory()
        mem_per = str(mem_usage.percent)
        #write all parameters in a file and return the filename
        f.write('Number of CPU: ' + cpu_no + '\n' + 'CPU Usage: ' + cpu_per + '%\n' + 'Memory Usage: ' + mem_per + '%/')
        f.close()
        return file_out


#find and send current CPU availablity based on usage percentage for node availability
def show_job_status():
        cpu_per = psutil.cpu_percent()
        data_out = 'busy'
        if cpu_per > 80.0:
                data_out = 'busy'
        else:
                data_out = 'ready'
        return data_out
#create socket and bind to address
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (NODE_IP, 10000)
print >> sys.stderr, 'Starting up on %s port %s' % server_address
try:
        sock.bind(server_address)
except socket.error as msg:
        print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
print 'Socket bind complete'
#listen for incoming connections
sock.listen(1)


#thread method
def clientThread(conn):
        try:
                print >> sys.stderr, 'connection from', client_address
                while True:
                        data = conn.recv(1024)
                        if data:
                                print >> sys.stderr, 'received "%s"' % data
                                if '.' in data:
                                        name = data.split('.')
                                        if name[-1] == 'py':
                                                data_out = file_handle_py(data)   #process .py
                                        elif name[-1] == 'c':
                                                data_out = file_handle_c(data) #process .c
                                        else:
                                                data_out = 'error_file'
                                                f = open(DIR + '/' + data_out, 'w')
                                                f.write('File type not supported')
                                                f.close()
                                elif data == 'status':
                                        data_out = show_status()
                                elif data == 'job_status':
                                        data_out = show_job_status()
                                else:
                                        data_out = 'error_file'
                                        f.open(DIR + '/' + data_out, 'w')
                                        f.write('Cannot read file')
                                        f.close()
                                print sys.stderr, 'sending data back to the client'
                                print sys.stderr, '%s' % data_out
                                conn.sendall(data_out)
                        else:
                                print >> sys.stderr, 'no more data from', client_address
                                break
        finally:
                conn.close()


#run server and wait for connection
while True:
        print >> sys.stderr, 'Waiting for a connection'
        conn, client_address = sock.accept()
        #start a new thread
        start_new_thread(clientThread,(conn,))
