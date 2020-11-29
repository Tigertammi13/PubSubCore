import threading
import socket
from queue import Queue
import pickle
import sys

host = socket.gethostname()
port = 55556

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
manager.connect((socket.gethostname(), 55555))

clients = []
identifiers = []
jobs = Queue(maxsize=100)
addresses = {}



def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message.decode("ascii"))
            job = {}
            job['type'] = 'INTERPRETER'
            job['client'] = addresses[client]
            job['code'] = message.decode('ascii')
            up = pickle.dumps(job)
            manager.send(up)
            #Queue.put(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.send(("Queue is full").encode("ascii"))
            del addresses[client]
            client.close()
            break

def receive_from_server():
    while True:
        message = manager.recv(1024)
        print(message)
        if (len(message) > 0):
            try:
                hello = message.decode("ascii")
                if  hello == "TYPE":
                    manager.send('UPLOADER'.encode('ascii'))
                if hello == "NAME":
                    manager.send('UP'.encode('ascii'))
            except:
                print('some other input')

def recieve():
    while True:
        client, address = server.accept()
        print(f'{address} has just connected')
        clients.append(client)
        client.send("WHO".encode('ascii'))
        msg = client.recv(1024).decode('ascii')
        addresses[client] = msg
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

thread = threading.Thread(target=receive_from_server)
thread.start()
print("The uploader is live")

recieve()
