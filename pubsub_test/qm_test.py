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
backups = {}
names = {}
busy = []
ids = {}


def push_messages():
    while True:
        if jobs.empty() != True:
            curr_job = jobs.get()
            curr_type = curr_job['type']
            if (curr_type in subscribers):
                for names1 in subscribers[curr_type]:
                    for serv in names[names1]:
                        if serv not in busy:
                            print(curr_job)
                            info = pickle.dumps(curr_job)
                            serv.send(info)
                            break
                        else:
                            pass
            jobs.task_done()


def pub(service):
    while True:
        try:
            info = service.recv(4096)
            try:
                msg = info.decode('ascii') 
                if msg == "BUSY":
                    if service not in busy:
                        busy.append(service)
                if msg == "FREE":
                    busy.remove(service)
            except: 
                if len(info) > 0:
                    job_todo = pickle.loads(info)
                    print('job: ', job_todo)
                    jobs.put(job_todo)
                    dateTimeObj = datetime.now()
                    timestampStr = dateTimeObj.strftime("%d-%b-%Y (%H:%M:%S.%f)")
                    with open('log.txt','a') as log:
                        log.write(timestampStr + " " +str(job_todo) + '\n')
        except:
            print('disconnected someone')
            its_type = services[service]
            its_name = ids[service]
            names[its_name].remove(service)
            del services[service]
            service.close()
            break


def sub():
    while True:
        service, address = server.accept()
        print(f'{address} has just connected')

        service.send('NAME'.encode("ascii"))
        name = service.recv(1024).decode('ascii')

        service.send('TYPE'.encode("ascii"))
        sub_type= service.recv(1024).decode('ascii')
        ids[service] = name
        if name in names:
            names[name].append(service)
        else:
            names[name]= []
            names[name].append(service)

        if sub_type in subscribers:
            if name not in subscribers[sub_type]:
                subscribers[sub_type].append(name)
        else:
            subscribers[sub_type] = []
            subscribers[sub_type].append(name)
        services[service] = sub_type


        thread = threading.Thread(target=pub, args=(service,))
        thread.start()
        
threading.Thread(target=push_messages).start()
threading.Thread(target=sub).start()
sub()
#jobs.join()
