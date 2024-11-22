import socket
import threading
import random
from config import CONFIG_PARAMS

# Configuration Parameters
WORKER0_IP_ADDRESS = CONFIG_PARAMS['WORKER0_IP_ADDRESS']
WORKER0_PORT = CONFIG_PARAMS['WORKER0_PORT']
WORKER1_IP_ADDRESS = CONFIG_PARAMS['WORKER1_IP_ADDRESS']
WORKER1_PORT = CONFIG_PARAMS['WORKER1_PORT']
EXIT_MESSAGE = CONFIG_PARAMS['EXIT_MESSAGE']

# Receive Message Method (Secondary Thread)
def receive_vector(client_socket: "socket.socket") -> None:
    try:
        while True:
            message = client_socket.recv(2048)
            if not message:
                break
            print('\r', end = '')
            print(f"Received: {message.decode('utf-8')}", end = '', flush = True )
            #print('Estado Vector:', message.decode('utf-8'), end = '', flush = True)
    except Exception as ex:
        print(f'Error receiving messages: {ex}')
    finally:
        client_socket.close()


# Start Client Method (Main Thread)
def start_client() -> None:
    print("Seleccione el algoritmo de ordenamiento:\n1. Mergesort\n2. Heapsort\n3. Quicksort")
    algorithm = int(input("Ingrese la opción: "))
    algorithm = {1: "mergesort", 2: "heapsort", 3: "quicksort"}[algorithm]

    n = int(input("Ingrese el tamaño del vector (ej. 10000): "))
    t = int(input("Ingrese el tiempo límite por worker (en segundos): "))
    vector = [random.randint(1, 100000) for _ in range(n)]
    task = {"vector": vector, "algorithm": algorithm, "time_limit": t}

    client0_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client0_socket.connect((WORKER0_IP_ADDRESS, WORKER0_PORT))
    client1_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client1_socket.connect((WORKER1_IP_ADDRESS, WORKER1_PORT))

    receive0_thread = threading.Thread(target = receive_vector, args = (client0_socket,))
    receive0_thread.daemon = True
    receive0_thread.start()

    receive1_thread = threading.Thread(target = receive_vector, args = (client1_socket,))
    receive1_thread.daemon = True
    receive1_thread.start()
    

    try:
        client0_socket.sendall(bytes(task).encode('utf-8'))
    except Exception as ex:
        print(f'Error sending messages: {ex}')
        client0_socket.close()


if __name__ == '__main__':
    start_client()