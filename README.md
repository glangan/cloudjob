# Job Management System

This system is designed to work on the Google Compute Engine platform.
All the functions should work on any other cloud platform except the starting or closing of new instance.

Running the system:

Web server: All the files in the folder should be placed in the web server root.
IP address in the cgi scripts should be changed to the local IP address of the server.
NFS should be configured to share ‘data’ folder.
Location of data folder on server is "WEB_SERVER_ROOT/data"

Server: All files should be placed in the home folder of the server.
IP addresses of server and nodes should be changed in the main_handler.py and 
then the script is run, it will start to listen for incoming connections.
Location of data folder should be changed in all the scripts.

Node: run_first script is run to mount the NFS drive.
Node.py is run and it will start to listen for incoming connections.
Location of data folder on node is "HOME/data"
The IP address of the web server should be provided to the client.


For Client:
1. Client enters IP address of web server on any browser.
2. The username and password to enter the system is 'test'.
3. Client can check if the system is running and the status of nodes by clicking 'Check' button.
4. After checking, user can upload a python script or a c file to run.
5. FIle will be uploaded and the result will be displayed on the browser.
