import socket
import pickle
import time
from algorithms import heapsort, quicksort, mergesort
from config import CONFIG_PARAMS

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']  
PORT = CONFIG_PARAMS['SERVER_PORT']
WORKER_0_IP = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']

def enviar_task(socket, data):
    serialized_data = pickle.dumps(data)
    length = len(serialized_data)
    socket.sendall(length.to_bytes(4, byteorder='big'))
    socket.sendall(serialized_data)

def recibir_task(socket):
    length = int.from_bytes(socket.recv(4), byteorder='big')
    task = b''
    while len(task) < length:
        paquete = socket.recv(length - len(task))
        if not paquete:
            raise Exception("Error: socket connection broken")
        task += paquete
    return pickle.loads(task)

def is_sorted(vector):
    return all(vector[i] <= vector[i + 1] for i in range(len(vector) - 1))


def handle_worker0(worker0_socket):
    try:
        print("WORKER 0 ESTA ENVIANDO DATOS ")
        task = recibir_task(worker0_socket)
        vector = task["vector"]
        algorithm = task["algorithm"]
        user_time_limit = task["time_limit"]
        extra = task["extra"]

        # Validación inicial
        if is_sorted(vector):
            enviar_task(worker0_socket, {"vector": vector, "completed": True})
            return

        
        start_time = time.time()
        end_time = start_time + user_time_limit

        while not is_sorted(vector):
            if algorithm == 1:
                print("Comenzando a ordenar con MERGESORT")
                extra = mergesort(vector, end_time, extra)
            elif algorithm == 2:
                print("Comenzando a ordenar con QUICKSORT")
                extra = quicksort(vector, end_time, extra)
            elif algorithm == 3:
                print("Comenzando a ordenar con HEAPSORT")
                extra = heapsort(vector, end_time, extra[1])

            if is_sorted(vector):
                print("Worker_1: VECTOR ORDENADO.")
                enviar_task(worker0_socket, {"vector": vector, "extra": extra, "completed": True})
                return 

            if time.time() >= end_time:
                print("Worker_1: TIEMPO AGOTADO. Devolviendo vector a Worker_0")
                enviar_task(worker0_socket, {"vector": vector, "extra": extra,  "completed": False})
                return 

    except Exception as e:
        print(f"Error en Worker_1: {e}")
    finally:
        worker0_socket.close()

def start_worker1():
    print(f"Worker_1 escuchando en {IP_ADDRESS}:{PORT}")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_ADDRESS, PORT))
    server_socket.listen(5)

    while True:
        worker0_socket, _ = server_socket.accept()
        print("Worker_1: Conexión establecida.")
        handle_worker0(worker0_socket)

if __name__ == "__main__":
    start_worker1()