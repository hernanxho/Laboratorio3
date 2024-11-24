import socket as sk
import threading as th
from config import CONFIG_PARAMS
from typing import List,Dict
import json as j

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS : list["sk.socket"] = []

def recibir_vector(client_socket: "sk.socket",address:"sk._RetAddress") -> None:
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
        except Exception as ex:
            print(f"Error de tipo: {ex}")

def start_server() -> None:
    
    server_socket1 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket1.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    server_socket1.bind((IP_ADDRESS, PORT))
    server_socket1.listen(MAX_CLIENTS)
    print("server1 conectado y escuchando")

    while True:

        client_socket, address = server_socket1.accept()
        client_thread = th.Thread(target = recibir_vector,args=(client_socket,address))
        client_thread.daemon = True
        client_thread.start()
        
        if client_socket:
            if client_socket not in LIST_OF_CLIENTS:
                LIST_OF_CLIENTS.append(client_socket)
            print(f"Clientes conectados a {address}")


if __name__ == '__main__':
    start_server()