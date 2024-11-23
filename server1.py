import socket as sk
import threading as th
from config import CONFIG_PARAMS
from typing import List

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
SERVER_IP_ADDRESS_WORKER0 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS = list["sk.socket"] = []

def start_server() -> None:
    
    server_socket1 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket1.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    server_socket1.bind((IP_ADDRESS, PORT))
    server_socket1.listen(MAX_CLIENTS)
    
    server_socket0 = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    server_socket0.connect((SERVER_IP_ADDRESS_WORKER0,PORT))
    print("conectado a worker0")

    print("Server1 iniciado worker1")


if __name__ == '__main__':
    start_server()