import socket
import pickle
import threading
import time
from algorithms import heapsort, quicksort, mergesort
from config import CONFIG_PARAMS

# Configuración del servidor
IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']  
PORT = CONFIG_PARAMS['SERVER_PORT']
WORKER_1_IP = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']

def enviar_task(socket, data):
    serialized_data = pickle.dumps(data)
    length = len(serialized_data)
    socket.sendall(length.to_bytes(4, byteorder='big'))
    socket.sendall(serialized_data)

def recibir_task(socket):
    longitud = int.from_bytes(socket.recv(4), byteorder='big')
    task = b''
    while len(task) < longitud:
        packet = socket.recv(longitud - len(task))
        if not packet:
            raise Exception("Error: socket connection broken")
        task += packet
    return pickle.loads(task)

def is_sorted(vector):
    return all(vector[i] <= vector[i + 1] for i in range(len(vector) - 1))

def handle_client(client_socket):
    try:
        print("CLIENTE ESTA ENVIANDO DATOS")
        task = recibir_task(client_socket)
        algorithm = task["algorithm"]
        vector = task["vector"]
        time_limit = task["time_limit"]
        
        if algorithm == 1:
            extra = [1, 0]
        elif algorithm == 2:
            extra = [(0, len(vector) - 1)]
        elif algorithm == 3:
            extra = [False, len(vector)]

        start_time = time.time()
        end_time = start_time + time_limit
        while not is_sorted(vector):
            if time.time() >= end_time:
                print("Worker_0: TIEMPO AGOTADO. Enviando al Worker_1...")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as worker1_socket:
                    worker1_socket.connect((WORKER_1_IP, PORT))
                    enviar_task(worker1_socket, {"algorithm": algorithm, "vector": vector, "time_limit": time_limit, "extra": extra})

                    # Recibir respuesta del Worker_1
                    task = recibir_task(worker1_socket)
                    vector = task["vector"]
                    if task["completed"]:
                        print("Worker_1 devolvió el vector completamente ordenado.")
                        break
                    else:
                        print("Worker_1 no completó el ordenamiento. Devolviendo el vector a Worker_0.")
                        extra = task["extra"]
            end_time = time.time() + time_limit
            # Ordenamiento de Worker_0
            if algorithm == 1:
                print("Comenzando a ordenar con MERGESORT")
                extra = mergesort(vector, end_time, extra)
            elif algorithm == 2:
                print("Comenzando a ordenar con QUICKSORT")
                extra = quicksort(vector, end_time, extra)
            elif algorithm == 3:
                print("Comenzando a ordenar con HEAPSORT")
                extra = heapsort(vector, end_time, extra[1])

        print("Worker_0: VECTOR ORDENADO")
        total_time = round(time.time() - start_time, 2)
        task = {"sorted_vector": vector, "time_taken": total_time}
        print(f"Enviando respuesta al cliente: Vector ordenado en {total_time} segundos.")
        enviar_task(client_socket, task)

    except Exception as e:
        print(f"Error en Worker_0: {e}")
    finally:
        client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP_ADDRESS, PORT))
    server_socket.listen(5)
    print(f"Worker_0 escuchando en {IP_ADDRESS}:{PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Conexión establecida con {client_address}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

if __name__ == "__main__":
    start_server()