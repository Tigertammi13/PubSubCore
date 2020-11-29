import socket
import threading

client_up = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_up.connect((socket.gethostname(), 55556))

client_down = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_down.connect((socket.gethostname(), 55557))

id = "Calc#1"

name = input('what is your name: ')


def recieve():
    while True:
        message = client_down.recv(1024).decode("ascii")
        print(message)
        if message == "WHO":
            myType = name
            client_down.send(myType.encode("ascii"))

def recieve2():
    while True:
        message = client_up.recv(1024).decode("ascii")
        print(message)
        if message == "WHO":
            myType = name
            client_up.send(myType.encode("ascii"))
        
def write():
    while True:
        code = f'{input()}'
        client_up.send(code.encode("ascii"))



write_thread = threading.Thread(target=write)
write_thread.start()


recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()

recieve_thread2 = threading.Thread(target=recieve2)
recieve_thread2.start()