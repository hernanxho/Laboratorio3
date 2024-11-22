import socket
import threading
import time
import algortimos
# Algoritmos de ordenamiento


def worker0():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8000))
    server.listen(1)
    print("Worker 0 listening on port 8000...")

    client_conn, addr = server.accept()
    print(f"Worker 0 connected to {addr}")

    data = client_conn.recv(4096).decode()
    task = eval(data)
    vector, algorithm, time_limit = task['vector'], task['algorithm'], task['time_limit']
    sort_func = {"mergesort": algortimos.merge_sort(), "heapsort": algortimos.heap_sort(), "quicksort": algortimos.quick_sort()}[algorithm]

    while True:
        start_time = time.time()
        while time.time() - start_time < time_limit:
            sort_func(vector)

        if sorted(vector) == vector:  # Verifica si está completamente ordenado
            client_conn.send(str({"status": "completed", "vector": vector}).encode())
            break

        print("Worker 0 sending to Worker 1...")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(('localhost', 8001))
            s.send(str({"vector": vector, "algorithm": algorithm}).encode())

        data = s.recv(4096).decode()
        task = eval(data)
        vector = task['vector']

    client_conn.close()
    server.close()

if __name__ == "__main__":
    worker0()