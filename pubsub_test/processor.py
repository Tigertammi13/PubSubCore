import socket
import threading
from io import StringIO
import pickle
import sys

manager = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
manager.connect((socket.gethostname(), 55555))

id = "Calc#1"


def recieve():
    while True:
        message = manager.recv(1024)
        print(message)
        try:
            msg = message.decode('ascii') 
            if msg == "TYPE":
                print('connected to manager')
                manager.send('INTERPRETER'.encode('ascii'))
            if msg == "NAME":
                manager.send('CALC'.encode('ascii'))
        except:
            if len(message) > 0:
                job_todo = pickle.loads(message)
                job_done ={}
                job_done['type'] = 'DOWNLOADER'
                job_done['client'] = job_todo['client']
                code = job_todo['code']
                old = sys.stdout
                temp = sys.stdout = StringIO()
                exec(code)
                sys.stdout = old
                job_done['result'] = temp.getvalue()
                try:
                    info = pickle.dumps(job_done)
                    manager.send(info)
                except:
                    print(f'dont work')





recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()