import threading
import socket
from queue import Queue

host = socket.gethostname()
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
identifiers = []
jobs = Queue(maxsize=100)

#chestiile mele
subscribers = {}
services = {}
log = open('log.txt','a')


def push_messages():
    while True:
        if jobs.empty() != True:
            curr_type = jobs.get()
            print(curr_type)
            if (curr_type in subscribers):
                for s in subscribers[curr_type]:
                    print(s)
                    s.send('hello sir'.encode('ascii'))
            jobs.task_done()


def pub(service):
    while True:
        try:
            job = service.recv(1024)
            if len(job) > 0:
                print('asta e job', job.decode('ascii'))
                jobs.put(job.decode('ascii'))
        except:
            print('l a scos')
            its_type = services[service]
            subscribers[its_type].remove(service)
            del services[service]
            service.close()
            break


def sub():
    while True:
        service, address = server.accept()
        print(f'{address} has just connected')
        service.send('TYPE'.encode("ascii"))
        sub_type = service.recv(1024).decode("ascii")
        if sub_type in subscribers:
            subscribers[sub_type].append(service)
        else:
            subscribers[sub_type] = []
            subscribers[sub_type].append(service)
        services[service] = sub_type
        thread = threading.Thread(target=pub, args=(service,))
        thread.start()
        
threading.Thread(target=push_messages).start()
threading.Thread(target=sub).start()
sub()
#jobs.join()
