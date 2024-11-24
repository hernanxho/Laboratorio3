import socket as sk
import threading as th
from config import CONFIG_PARAMS
from typing import List,Dict
import json as j

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']
SERVER_IP_ADDRESS_WORKER1 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS : List["sk.socket"] = []


def recibir_vector(client_socket: "sk.socket",address:"sk._RetAddress",server : "sk.socket") -> None:
        try:

            task = client_socket.recv(32000000)
            task = task.decode('utf-8')
            print("Tarea recibida")

            task_dict = j.loads(task)
            for i in task_dict["vector"]:
                 print("Numero recibido: "+str(i))
            print("Tiempo: "+str(task_dict["time_limit"]))
            print("Ordenamiento:" +str(task_dict["ordenamiento"]))
            task = bytes(task,'utf-8')
            client_socket.sendall(task)
            server.sendall(task)
 
        except Exception as ex:
            print(f"Error de tipo: {ex}")


def start_server() -> None:
    server_socket0 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket0.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    server_socket0.bind((IP_ADDRESS, PORT))
    server_socket0.listen(MAX_CLIENTS)
    print("Server0 iniciado y escuchando ")

    server_socket1 = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    server_socket1.connect((SERVER_IP_ADDRESS_WORKER1,PORT))
    print("conectado a worker1")

    while True:
        client_socket, address = server_socket0.accept()
        client_thread = th.Thread(target= recibir_vector,args= (client_socket,address,server_socket1))
        client_thread.daemon = True
        client_thread.start()
        
        server1_thread = th.Thread(target= recibir_vector,args= (server_socket1,address,client_socket))
        server1_thread.daemon = True
        server1_thread.start()
        
        if client_socket:
            if client_socket not in LIST_OF_CLIENTS:
                LIST_OF_CLIENTS.append(client_socket)
            print(f"Clientes conectados a {address}")

if __name__ == '__main__':
    start_server()