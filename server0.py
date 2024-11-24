import socket as sk
import threading as th
from config import CONFIG_PARAMS
from typing import List
import algorithm as alg
import time
import json as j

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']
SERVER_IP_ADDRESS_WORKER1 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS : List["sk.socket"] = []

def recibir_vector(socket_1: "sk.socket", address: "sk._RetAddress", socket_2: "sk.socket", orden) -> None:
    try:
        task = socket_1.recv(32000000)
        task = task.decode('utf-8')
        print("Tarea recibida")

        # Parse the JSON string into a dictionary
        task_dict = j.loads(task)

        if task_dict["ordenamiento"] == "mergesort":
            task_dict["vector"], task_dict = alg.merge_sort_iterative(task_dict["vector"], int(task_dict["time_limit"]), task_dict)
        elif task_dict["ordenamiento"] == "quicksort":
            task_dict["vector"], task_dict = alg.quick_sort_iterative(task_dict["vector"], int(task_dict["time_limit"]), task_dict)
        elif task_dict["ordenamiento"] == "heapsort":
            task_dict["vector"], task_dict = alg.heap_sort_iterative(task_dict["vector"], int(task_dict["time_limit"]), task_dict)

        for i in task_dict["vector"]:
            print("Numero recibido: " + str(i))
        print("Tiempo: " + str(task_dict["time_limit"]))
        print("Ordenamiento: " + str(task_dict["ordenamiento"]))
        task = bytes(task, 'utf-8')

        if orden:
            if task_dict["estado"]:
                socket_1.sendall(task)
            else:
                socket_2.sendall(task)
        else:
            if task_dict["estado"]:
                socket_2.sendall(task)
            else:
                socket_1.sendall(task)

    except Exception as ex:
        print(f"Error de tipo: {ex}")


def start_server() -> None:
    server_socket0 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket0.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    server_socket0.bind((IP_ADDRESS, PORT))
    server_socket0.listen(MAX_CLIENTS)
    print("Server1 conectado y escuchando")

    server_socket1 = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    server_socket1.connect((SERVER_IP_ADDRESS_WORKER1,PORT))
    print("Conectado a worker1")

    while True:
        client_socket, address = server_socket0.accept()
        client_thread = th.Thread(target = recibir_vector, args = (client_socket, address, server_socket1, True))
        client_thread.daemon = True
        client_thread.start()

        server1_thread = th.Thread(target = recibir_vector, args = (server_socket1, address, client_socket, False))
        server1_thread.daemon = True
        server1_thread.start()

        if client_socket:
            if client_socket not in LIST_OF_CLIENTS:
                LIST_OF_CLIENTS.append(client_socket)
            print(f"Cliente conectado a {address}")

if __name__ == '__main__':
    start_server()