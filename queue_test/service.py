import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((socket.gethostname(), 55555))
id = "Calc#1"


def recieve():
    while True:
        message = client.recv(1024).decode("ascii")
        print(message)
        if message == "TYPE":
            myType = f'{input()}'
            client.send(myType.encode("ascii"))

def write():
    while True:
        mesage = f'{input()}'
        client.send(mesage.encode("ascii"))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
