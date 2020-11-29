import threading
import socket
from queue import Queue
import pickle
from datetime import datetime

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
            curr_job = jobs.get()
            curr_type = curr_job['type']
            if (curr_type in subscribers):
                for s in subscribers[curr_type]:
                    print(s)
                    info = pickle.dumps(curr_job)
                    s.send(info) 
            jobs.task_done()


def pub(service):
    while True:
        try:
            info = service.recv(4096)
            if len(info) > 0:
                job_todo = pickle.loads(info)
                print('job', job_todo['type'])
                jobs.put(job_todo)
        except:
            print('disconnected someone')
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
        sub_type = service.recv(1024).decode('ascii')
        print (sub_type)
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
