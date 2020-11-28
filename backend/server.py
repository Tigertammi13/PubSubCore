import threading
import socket
from queue import Queue

host = '127.0.0.1'
port = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
identifiers = []
jobs = Queue(maxsize=100)


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(message)
            #Queue.put(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.send(("Queue is full").encode("ascii"))
            client.close()
            identifier = identifiers[index]
            broadcast(f'{identifier} finnished task'.encode('ascii'))
            identifiers.remove(identifier)
            break


def recieve():
    while True:
        client, address = server.accept()
        print(f'{address} has just connected')
        client.send("WHO".encode("ascii"))
        identifier = client.recv(1024).decode("ascii")
        identifiers.append(identifier)
        clients.append(client)
        print(f'{identifier}'+ " is now ready to work")

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print("The queue is live")
recieve()
