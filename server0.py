import socket as sk
import threading as th
from config import CONFIG_PARAMS
from typing import List

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']
SERVER_IP_ADDRESS_WORKER1 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS : List["sk.socket"] = []

def start_server() -> None:
    server_socket0 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket0.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    server_socket0.bind((IP_ADDRESS, PORT))
    server_socket0.listen(MAX_CLIENTS)
    print("Server0 iniciado ")

    server_socket1 = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    server_socket1.connect((SERVER_IP_ADDRESS_WORKER1,PORT))
    print("conectado a worker1")

    while True:
        client_socket, address = server_socket0.accept()
        if client_socket:
            if client_socket not in LIST_OF_CLIENTS:
                LIST_OF_CLIENTS.append(client_socket)
            print(f"Cliente conectado a {address}")

if __name__ == '__main__':
    start_server()
