import socket
from sys import argv
import signal 
import sys

UDP_HOST = "" # Means all available interfaces
UDP_PORT = 0 # Arbitrary port, so that OS will assign

# statistics
msgsReceived = 0
bytesReceived = 0

#Timeout is in miliseconds
script,fileName,timeout = argv

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind((UDP_HOST, UDP_PORT))

UDP_HOST, UDP_PORT = sock.getsockname()


####################### Write port number to a file ###################################
f = open("port","w+")
f.write(str(UDP_PORT))
f.close()
#######################################################################################

print("Listening at:", UDP_PORT)

# First message will be 1024 btes fixed, everything after depends on metadata
data,addr = sock.recvfrom(1024)
expected_FileSize = data[0]
bufferSize = data[1]

expectedMsgs = int(expected_FileSize/bufferSize)

# Open up the file to store stuff
f=open(fileName,'wb')

try:
	sock.settimeout(int(timeout)/1000)
	while msgsReceived != expectedMsgs:
	    data, addr = sock.recvfrom(bufferSize)
	    msgsReceived += 1
	    f.write(data)	    
except socket.timeout:
	print("Socket timed out")
finally:
	print("Received # of msgs: ", msgsReceived)
	print("Bytes received: ", len(data))
	f.close()
	sock.close()
	sys.exit()