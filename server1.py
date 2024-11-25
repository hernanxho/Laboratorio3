import socket as sk   #ES ESTE
import threading as th
from config import CONFIG_PARAMS
from typing import List
import algorithm as alg
import json as j

IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
SERVER_IP_ADDRESS_WORKER0 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']
PORT = CONFIG_PARAMS['SERVER_PORT']
MAX_CLIENTS = CONFIG_PARAMS['SERVER_MAX_CLIENTS']
LIST_OF_CLIENTS : list["sk.socket"] = []

def recibir_vector(socket_1: "sk.socket", address: "sk._RetAddress", socket_2: "sk.socket", orden: bool) -> None:
    #try:
        task = socket_1.recv(32000000)  # Recibir la tarea
        if not task:
            return
        
        task = task.decode('utf-8')
        print("Tarea recibida")

        # Parsear la cadena JSON a un diccionario
        task_dict = j.loads(task)
        


        # Empezar a ordenar según el tipo de algoritmo
        if task_dict["ordenamiento"] == "mergesort":
            task_dict["vector"], task_dict = alg.merge_sort_iterative(task_dict["vector"], float(task_dict["time_limit"]), task_dict)
        elif task_dict["ordenamiento"] == "quicksort":
            task_dict["vector"], task_dict = alg.quick_sort_iterative(task_dict["vector"], float(task_dict["time_limit"]), task_dict)
        elif task_dict["ordenamiento"] == "heapsort":
            task_dict["vector"], task_dict = alg.heap_sort_iterative(task_dict["vector"], float(task_dict["time_limit"]), task_dict)

        # Marcar el último worker que procesó la tarea
        task_dict["ult_worker"] = IP_ADDRESS
        # Contar cantidad rebotes
        task_dict["rebotes"] += 1

        # Imprimir los números y detalles de la tarea
        #for i in task_dict["vector"]:
            #print(f"Numero recibido: {i}")
        print(f"Tiempo límite: {task_dict['time_limit']}")
        print(f"Cantidad de elementos: {len(task_dict['vector'])}")
        print(f"Ordenamiento: {task_dict['ordenamiento']}")
        print(f"# rebote: {task_dict['rebotes']}")
        print(f"Estado del ordenamiento: {task_dict['estado']}")
        print(f"Último worker: {task_dict['ult_worker']} \n\n")
        
        # Convertir el diccionario de vuelta a JSON para enviarlo
        task = j.dumps(task_dict)
        task = bytes(task, 'utf-8')

        # Verificación de estado y enviar el resultado
        if task_dict["estado"]:  # Si la tarea está completa
            if orden:
                socket_1.sendall(task)  # Enviar al servidor original
            else:
                socket_2.sendall(task)  # Enviar al otro servidor
        else:
            if orden:
                socket_2.sendall(task)  # Enviar al servidor siguiente
            else:
                socket_1.sendall(task)  # Enviar al servidor anterior

    #except Exception as ex:
        #print(f"Error de tipo: {ex}")
        #print(f"Tarea incompleta, reintentando...")

def start_server() -> None:
    # Crear socket para el servidor 1
    server_socket1 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    server_socket1.setsockopt(sk.SOL_SOCKET, sk.SO_REUSEADDR, 1)
    server_socket1.bind((IP_ADDRESS, PORT))     
    server_socket1.listen(MAX_CLIENTS)
    print("Server1 conectado y escuchando")

    # Crear socket para el servidor 0 y conectarse a él
    #server_socket0 = sk.socket(sk.AF_INET, sk.SOCK_STREAM)
    #server_socket0.connect((SERVER_IP_ADDRESS_WORKER0, PORT))  # Conectar con el segundo servidor

    
    while True:

        # Aceptar conexiones de clientes
        client_socket, address = server_socket1.accept()
        # Agregar cliente a la lista
        if client_socket:
            if client_socket not in LIST_OF_CLIENTS:
                LIST_OF_CLIENTS.append(client_socket)
            print(f"Clientes conectados a {address}")    

        # Crear hilos para recibir datos y procesarlos
        if len(LIST_OF_CLIENTS) > 1:
            client_thread = th.Thread(target = recibir_vector, args = (LIST_OF_CLIENTS[1], address, LIST_OF_CLIENTS[0], True))
            client_thread.daemon = True
            client_thread.start()

            server0_thread = th.Thread(target = recibir_vector, args = (LIST_OF_CLIENTS[0], address, LIST_OF_CLIENTS[1], False))
            server0_thread.daemon = True
            server0_thread.start()

if __name__ == '__main__':
    start_server() #ES ESTE