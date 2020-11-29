import threading
import socket
from queue import Queue
import pickle


host = socket.gethostname()
port = 55557

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
manager.connect((socket.gethostname(), 55555))

clients = []
identifiers = []
jobs = Queue(maxsize=100)
addresses = {}



def receive_from_server():
    while True:
        message = manager.recv(1024)
        print(message)
        try:
            msg = message.decode('ascii') 
            if msg == "TYPE":
                print('connected to manager')
                manager.send('DOWNLOADER'.encode('ascii'))
            if msg == "NAME":
                manager.send('DOWN'.encode('ascii'))
        except:
            if len(message) > 0:
                finished_job = pickle.loads(message)
                target = finished_job['client']
                try:
                    addresses[target].send(finished_job['result'].encode('ascii'))
                except:
                    print(f'client{target} has disconnected')

def recieve():
    while True:
        client, address = server.accept()
        print(f'{address} has just connected')
        clients.append(client)
        client.send("WHO".encode('ascii'))
        msg = client.recv(1024).decode('ascii')
        addresses[msg] = client


print("The downloader is live")
thread = threading.Thread(target=receive_from_server)
thread.start()
recieve()
