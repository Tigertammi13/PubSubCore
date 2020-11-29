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
        """
        message1 = ""
        while len(message1) == 0:
            message1 = f'{input()}'
            client.send(message1.encode("ascii"))
        """

def write():
    while True:
        message = f'{input()}'
        client.send(message.encode("ascii"))



write_thread = threading.Thread(target=write)
write_thread.start()


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()