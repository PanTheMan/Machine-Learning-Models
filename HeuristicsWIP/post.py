import socket
import sys
import os

MESSAGE = b"Hello, World!"
script,UDP_HOST,UDP_PORT,payload,fileName = sys.argv

#convert to integers
UDP_PORT = int(UDP_PORT)
payload = int(payload)

print("UDP target HOST:", UDP_HOST)
print("UDP target port:", UDP_PORT)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP


# Open file
f = open(fileName,"rb")
fileSize = os.path.getsize(fileName)
print(fileSize)
data=f.read(payload)

##### Send Meta Data ########################
meta = bytearray()
meta.append(fileSize)
meta.append(payload)
sock.sendto(meta,(UDP_HOST,UDP_PORT))


#############################################

while data:
	sock.sendto(data,(UDP_HOST,UDP_PORT))
	print("sending....")
	data=f.read(payload)
f.close()
sock.close()