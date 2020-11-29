import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 55555))
id = "Pub#1"

msg=""
while msg!="exit":
    msg=input()
    client.send(msg.encode("ascii"))