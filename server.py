#  coding: utf-8 
import SocketServer
import os.path
import webbrowser

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# Modified 2016 Han Wang, Xi Zhang
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
	
	self.data_list = self.data.split()

	print self.data.strip() + '\n'

	if len(self.data_list)>0 and self.data_list[0]== 'GET':
	    
	    self.file_name = self.data_list[1]

	    self.path = "./www" + self.file_name

	    path_found, path_type, path_new = self.findPath(self.path)
	    if (path_found):
		    
		self.path = path_new
		if (path_type == 1):
		    if self.path[-4:] == ".css":
			self.file_type = "text/css"
		    elif self.path[-5:] == ".html":
			self.file_type = "text/html"
		elif (path_type == 0):
		    self.path += "index.html"
		    self.file_type = "text/html" 

		# reference: http://stackoverflow.com/questions/14606799/what-does-r-do-in-the-following-script
		try:
		    f = open(self.path, "r")
		    dataToSend = f.read()
		    f.close()
		    self.request.send("HTTP/1.1 200 OK\r\n")
		    self.request.send('content-type: '+self.file_type+ '\r\n\r\n')
		    self.request.send(dataToSend + '\r\n')

		except: 
		    self.throwError()
    
	    else:
		self.throwError()

		
    def throwError(self):
	self.head = "HTTP/1.1 "
	self.error_msg = "404 NOT FOUND\n"
	self.request.send(self.head + self.error_msg + '\r\n\r\n')
	self.request.send(self.error_msg)	
    
    def findPath(self, fpath):
	self.found = False
	self.dir_or_file = -1
	
	# reference: http://stackoverflow.com/questions/8933237/how-to-find-if-directory-exists-in-python

	fpath = os.path.abspath(fpath)
	if ('www' in fpath):  
	    if (fpath[-1]=='/'):
		self.found = os.path.isdir(fpath)
		if self.found:
		    self.dir_or_file = 0
		else:
		    fpath = fpath.rstrip('/')
		    self.found = os.path.isfile(fpath)
		    if self.found:
			self.dir_or_file = 1
	    else:
		self.found = os.path.isfile(fpath)
		if self.found:
		    self.dir_or_file = 1
		else:
		    fpath += '/'
		    self.found = os.path.isdir(fpath)
    
		    if self.found:
			self.dir_or_file = 0
		
	return (self.found, self.dir_or_file, fpath)
	

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
