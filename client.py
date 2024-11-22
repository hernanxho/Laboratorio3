import socket
import random

def client():
    print("Seleccione el algoritmo de ordenamiento:\n1. Mergesort\n2. Heapsort\n3. Quicksort")
    algorithm = int(input("Ingrese la opción: "))
    algorithm = {1: "mergesort", 2: "heapsort", 3: "quicksort"}[algorithm]

    n = int(input("Ingrese el tamaño del vector (ej. 10000): "))
    t = int(input("Ingrese el tiempo límite por worker (en segundos): "))

    vector = [random.randint(1, 100000) for _ in range(n)]

    task = {"vector": vector, "algorithm": algorithm, "time_limit": t}

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(('localhost', 8000))  # Conecta con Worker 0
        client_socket.send(str(task).encode())

        while True:
            response = client_socket.recv(4096).decode()
            if not response:
                break
            result = eval(response)
            if result['status'] == "completed":
                print("Vector ordenado correctamente.")
                print(f"Vector ordenado: {result['vector'][:10]}...")  # Mostrar solo primeros 10 elementos
                break

if __name__ == "__main__":
    client()