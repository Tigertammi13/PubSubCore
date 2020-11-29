import socket
import threading
import time

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 55555))
id = "Pub#1"


jobs=["#small 5 3","#medium 10 -3","#small 3 0","#big 15 100"]

for i in range(1):
    client.send(jobs[i].encode("ascii"))