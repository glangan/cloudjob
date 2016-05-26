import socket
import sys
from thread import *
import threading
import Queue
import os
import time
import errno
from instance_handler import *

NODE_1 = '10.240.125.75'
NODE_2 = '10.240.149.254'
SERVER_ADD = '10.240.105.92'
NODE_PORT = 10000   #Port number of node
DIR = '/var/www/html/data/'   #location of data stored in server
#nodes list
nodes = [NODE_1, NODE_2]   # local IP addresses of nodes
#jobs list
jobs = Queue.PriorityQueue()


############## Methods ###############
#Sends socket, takes node, message and a queue as input (see below)
def socket_send(node, message, q):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
                s.connect((node, NODE_PORT))
                #send data
        except socket.error, v:
                errorcode = v[0]
                if errorcode == errno.ECONNREFUSED:
                        print "Connection refused"
        try:
                s.sendall(message)
                data_recv = s.recv(1024)
        except socket.error, e:
                if isinstance(e.args, tuple):
                        print "errno is %d" % e[0]
                        if e[0] == errno.EPIPE:
                                print "Detected remote disconnect"
                        else:
                                pass
                else:
                        print "Socket error ", e
        finally:
                s.close()
        q.put(data_recv)


def update_all_stats(message):
        threads = []   #store threads in a list
        node_status_data = ''
        #A queue is used in this case to get return values from the thread, socket_send function
        #stores the output in the queue and it can be accessed by this function using queue.get()
        #also python
        q = Queue.Queue()
        for node in nodes:
                t = threading.Thread(target=socket_send, args=(node, message, q))
                threads.append(t)
        #start all threads
        for x in threads:
                x.start()
        #wait for all threads
        for x in threads:
                x.join()
        while not q.empty():
                file_in = q.get()
                f = open(DIR + file_in, 'r')
                node_status_data += f.read()
                f.close()
                os.remove(DIR + file_in)
        #write received data to a file
        status_data = 'all_stats'
        f = open(DIR + status_data, 'a+')
        f.write(node_status_data)
        f.write('Number of jobs in queue: ' + str(jobs.qsize()))
        f.close()
        #return name of the file
        return status_data

################## Job Scheduling ######################
def start_new_job(file_in):
        msg_queue = Queue.Queue()
        file_priority = file_in[0]
        file_name = file_in[1:]
        file_pq = (int(file_priority), file_name)
        jobs.put(file_pq)   #put job in a queue
        print sys.stderr, 'Jobs in queue: %s' % jobs.qsize()
        # Monitor size of job queue, if queue is more than a certain number, start a new node
        if jobs.qsize() > 10:
                create_new_instance()
        elif jobs.qsize() <= 10 and len(nodes) > 2:
                delete_extra_instance()
        while not jobs.empty():
                node = get_node()   #get node or wait: if all nodes are busy, execution waits here,
                file_p, file_send = jobs.get()   #get the first task from queue
                t = threading.Thread(target=socket_send, args=(node, file_send, msg_queue)).start()
                file_out = msg_queue.get()
        return file_out


#check node availability
def node_available(node):
        q = Queue.Queue()
        message = 'job_status'   #message to send
        t = threading.Thread(target=socket_send, args=(node, message, q)).start()
        return q.get()
#get available node
def get_node():
        node_dict = {node : node_available(node) for node in nodes}   #store node and avaialability in a dictionary {node : availability}
        print sys.stderr, 'Node 1: %s' % node_dict[nodes[0]]
        print sys.stderr, 'Node 2: %s' % node_dict[nodes[1]]
        #send one node that is available
        #if both nodes are unavailable, run this function again after 10 second
        for key, val in node_dict.items():
                if val == 'ready':
                        return key
                else:
                        time.sleep(10)
                        get_node()


#################Instance Methods ######################
def create_new_instance():
        credentials = GoogleCredentials.get_application_default()
        compute = build('compute', 'v1', credentials=credentials)
        r = create_instance(compute, 'grand-reference-93404', 'asia-east1-b', 'node-3')
        if 'errors' not in r:
                while True:
                        instances = list_instances(compute, 'grand-reference-93404', 'asia-east1-b')
                        time.sleep(15)
                        for instance in instances:
                                if instance['name'] == 'node-3':
                                        if instance['status'] == 'running':
                                                break
        instances = list_instances(compute, 'grand-reference-93404', 'asia-east1-b')
        for instance in instances:
                if instance['name'] == 'node-3':
                        node_ip = instance['networkInterfaces'][0]['networkIP']
                        nodes.append(node_ip)
def delete_extra_instance():
        credentials = GoogleCredentials.get_application_default()
        compute = build('compute', 'v1', credentials=credentials)
        delete_instance(compute, 'grand-reference-93404', 'asia-east1-b', 'node-3')
        del nodes[-1]


#create socket and bind to address
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (SERVER_ADD, 11000)
print >> sys.stderr, "starting up on %s port %s" % server_address
try:
        sock.bind(server_address)
except socket.error as msg:
        print 'Bind failed. Error Code: ' + str(msg[0]) + ' Message ' + msg[1]
        sys.exit()
print 'socket bind complete'
#listen for incoming connection
sock.listen(1)

#Thread Method to handle each incoming connection from cgi script
def clientThread(conn):
        try:
                print >> sys.stderr, 'connection from', client_address
                while True:
                        data = conn.recv(1024)
                        if data:
                                print >> sys.stderr, 'received %s' % data
                                if client_address[0] == SERVER_ADD:
                                        if data == 'status':
                                                file_out = update_all_stats(data)
                                        else:
                                                file_out = start_new_job(data)
                                print >> sys.stderr, 'Sending data back to client'
                                print >> sys.stderr, '%s' % file_out
                                conn.sendall(file_out)
                        else:
                                print >> sys.stderr, 'No more data from ', client_address
                                break
        finally:
                conn.close()
while True:
        print >> sys.stderr, 'Waiting for connection'
        conn, client_address = sock.accept()
        #start a new thread
        start_new_thread(clientThread, (conn,))
