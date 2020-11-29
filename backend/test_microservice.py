import socket
import threading

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 5555))
id = "Calc#1"


def recieve():
    while True:
        try:
            message = client.recv(10).decode("ascii")
            if message == "WHO":
                client.send(id.encode("ascii"))
            else:
                print(message.decode("ascii"))
        except:
            print("An error occured".encode("ascii"))
            client.close()
            break


def write():
    while True:
        mesage = f'{input()}'
        client.send(mesage.encode("ascii"))


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
