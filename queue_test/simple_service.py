import socket
import threading
import time

client=""
def connect():
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((socket.gethostname(), 55555))
id = "Serv#1"

def respond():
    while True:
            message=""
            print("Waiting...")
            # Get a job
            message = client.recv(1024).decode("ascii")
            while message!="":
                    print(message)
                    values=message.split()
                    print(values[0], values[1], values[2])
                    #Simulate execution
                    time.sleep(int(values[1]))
                    #Send the result
                    client.send(str(values[2]).encode("ascii"))
                    message=""

                    # print("Upsie daysie")
                    client.close()
                    connect()       #After we got the job we got kicked from the server, now we must reconnect
                                    #to signal that we are avaiable



connect()


respond_thread = threading.Thread(target=respond)
respond_thread.start()


