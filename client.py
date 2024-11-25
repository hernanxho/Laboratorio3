import socket
import pickle
from config import CONFIG_PARAMS

# Configuración del cliente
SERVER_IP_ADDRESS = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']    
SERVER_PORT = CONFIG_PARAMS['SERVER_PORT']

def enviar_task(socket, task):
    serialized_task = pickle.dumps(task)
    length = len(serialized_task)
    socket.sendall(length.to_bytes(4, byteorder='big'))  # Enviar el tamaño
    socket.sendall(serialized_task)  # Enviar los datos

def recibir_task(socket):
    length = int.from_bytes(socket.recv(4), byteorder='big')
    task = b''
    while len(task) < length:
        packet = socket.recv(length - len(task))
        if not packet:
            raise Exception("Error: socket connection broken")
        task += packet
    return pickle.loads(task)


def start_client(vector, tiempo, tipo):
    """Inicia el cliente y se conecta al servidor."""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP_ADDRESS, SERVER_PORT))
        print("Conectado al servidor principal (worker_0).")

            

        task = {
                "algorithm": tipo,
                "vector": vector,
                "time_limit": float(tiempo)
            }
        enviar_task(client_socket, task)
        print("Esperando respuesta del servidor...")
        task_recibida = recibir_task(client_socket)
        guardar(task_recibida["sorted_vector"], 'ordenado.txt')
        print(f"Vector ordenado recibido y guardado en -{'ordenado.txt'}-.")
        print(f"Tiempo total: {task_recibida['time_taken']} segundos")

    except Exception as e:
        print(f"Error inesperado: {e}")
    finally:
        client_socket.close()

def guardar(lista, nombre_archivo):
    with open(nombre_archivo, 'w') as archivo:
        for numero in lista:
            archivo.write(f"{numero}\n")



