import socket
import time
import algortimos

def worker1():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('localhost', 8001))
    server.listen(1)
    print("Worker 1 listening on port 8001...")

    while True:
        client_conn, addr = server.accept()
        print(f"Worker 1 connected to {addr}")

        data = client_conn.recv(4096).decode()
        task = eval(data)
        vector, algorithm = task['vector'], task['algorithm']
        sort_func = {"mergesort": algortimos.merge_sort(), "heapsort": algortimos.heap_sort(), "quicksort": algortimos.quick_sort()}[algorithm]

        start_time = time.time()
        time_limit = task.get('time_limit', 5)  # Usa 5 segundos como tiempo por defecto
        while time.time() - start_time < time_limit:
            sort_func(vector)

        if sorted(vector) == vector:  # Verifica si está completamente ordenado
            client_conn.send(str({"status": "completed", "vector": vector}).encode())
        else:
            print("Worker 1 sending back to Worker 0...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(('localhost', 8000))
                s.send(str({"vector": vector, "algorithm": algorithm}).encode())

        client_conn.close()

if __name__ == "__main__":
    worker1()