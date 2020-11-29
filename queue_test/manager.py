import threading
import socket
from queue import Queue

host = socket.gethostname()
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()



jobs = Queue(maxsize=100)

# chestiile mele
subscribers = {}
services = []
identifiers = []
log = open('log.txt', 'a')


def print_queue(queue):
    for element in list(queue.queue):
        print(element,end=" ")
    print()

def print_services(serv):
    print("Currently we have these services")
    for s in serv:
        print(s)

def recieve_jobs():
    while True:
        if jobs.empty() != True:
            job=jobs.get()
            if len(services)>0:
                service=services[0]
                print(service)
                print("We are dipatching:",job," to ",service," out you go")
                service.send(job.encode("ascii"))
                index=services.index(service)
                print("Removing the service on position ",index)
                services.remove(index)
                service.close()

            else:
                print("Waiting for a free service")

def pub(service):
    while True:
        try:
            job = service.recv(1024)
            job=job.decode("ascii")
            if job[0]!='#':
                print("Job done we got: ",job)
            else:
                if job=="stop":
                        server.close()
                        exit(0)
                if len(job) > 0:
                    print('we got a job:', job)
                    jobs.put(job)
                    print("The current queue: ")
                    print_queue(jobs)


        except:
            print('l a scos')
            out=services.index(service)
#            services.remove(out)
            service.close()
            break


def sub():
    while True:
        service, address = server.accept()
        print_services(services)
        print(f'{address} has just connected')
        message=service.recv(1024)
        if len(message)!=10: ### This must separate publisers froms ervicies which are listening
            services.append(service)
            thread = threading.Thread(target=pub, args=(service,))
            thread.start()

print("Server started")
threading.Thread(target=recieve_jobs).start()
threading.Thread(target=sub).start()
sub()
# jobs.join()
