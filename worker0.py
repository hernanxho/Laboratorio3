import socket
import threading
from config import CONFIG_PARAMS
from typing import List

# Configuration Parameters
WORKER0_IP_ADDRESS = CONFIG_PARAMS['WORKER0_IP_ADDRESS']
WORKER0_PORT = CONFIG_PARAMS['WORKER0_PORT']
WORKER1_IP_ADDRESS = CONFIG_PARAMS['WORKER1_IP_ADDRESS']
WORKER1_PORT = CONFIG_PARAMS['WORKER1_PORT']
EXIT_MESSAGE = CONFIG_PARAMS['EXIT_MESSAGE']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS: List["socket.socket"] = []

# Remove Client from List of Clients
def remove_client(client_socket: "socket.socket") -> None:
    if client_socket in LIST_OF_CLIENTS:
        LIST_OF_CLIENTS.remove(client_socket)


# Attemp to Broadcast a Client Message
def broadcast(message: bytes, client_socket: "socket.socket") -> None:
    for client in LIST_OF_CLIENTS:
        if client != client_socket:
            try:
                client.sendall(message)
            except Exception as ex:
                client.close()
                remove_client(client)


# Handle Client Method (Clients Secondary Threads)
def handle_client(client_socket: "socket.socket", client_address: "socket._RetAddress") -> None:
    try:
        client_socket.sendall(b'Conected to Worker0...')
        while True:
            message = client_socket.recv(2048)
            if not message:
                remove_client(client_socket)
                break
            print(f'<{client_address[0]}>', message.decode('utf-8'))
            message_to_send = bytes(f'<{client_address[0]}> {message.decode('utf-8')}', 'utf-8')
            broadcast(message_to_send, client_socket)
    except Exception as ex:
        print(f'Error on client {client_address[0]}: {ex}')
        remove_client(client_socket)
    finally:
        client_socket.close()


# Start Server Method (Main Thread)
def start_worker0() -> None:
    worker0_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker0_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    worker0_socket.bind((IP_ADDRESS, PORT))
    #worker0_socket.listen(MAX_CLIENTS)

    worker1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    worker1_socket.connect((WORKER1_IP_ADDRESS, WORKER1_PORT))

    print(f'Worker0 started at {IP_ADDRESS}:{PORT} and listening...')

    try:
        while True:
            client_socket, client_address = worker0_socket.accept()
            LIST_OF_CLIENTS.append(client_socket)
            print(client_address[0], 'connected')

            client_thread = threading.Thread(target = handle_client, args = (client_socket, client_address))
            client_thread.daemon = True
            client_thread.start()
    except Exception as ex:
        print(f'Error accepting clients: {ex}')
        print('Closing the server...')
    finally:
        for client in LIST_OF_CLIENTS:
            client.close()
        worker0_socket.close()


if __name__ == '__main__':
    start_worker0()