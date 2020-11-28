from flask import Flask
from flask import request
from queue import Queue
import socket
import threading
name = "PubSubCore"
app = Flask(name)




@app.route('/', methods=['GET'])
def homepage():
    result = ""
    with open("./frontend/welcome.html") as file:
        return file.read()

@app.route('/', methods=['POST'])
def page2():
    req = request.form
    print(req['sum_of'].split())
    return "asdsad"


if name == 'main':
    app.run(use_reloader=True, debug=True)
