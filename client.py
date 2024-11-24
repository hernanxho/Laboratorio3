import socket as sk
import threading as th
from config import CONFIG_PARAMS

SERVER_IP_ADDRESS_WORKER0 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER0']
SERVER_IP_ADDRESS_WORKER1 = CONFIG_PARAMS['SERVER_IP_ADDRESS_WORKER1']
SERVER_PORT = CONFIG_PARAMS['SERVER_PORT']
EXIT_MESSAGE = CONFIG_PARAMS['EXIT_MESSAGE']


def receive_vector(client_socket: "sk.socket",nWork) -> None:
    try:
        while True:
            vector= client_socket.recv(32000000)
            if not vector:
                break
            vector.decode('utf-8')
            if(nWork==True):
                print("El worker0 ha mandado este vector")
            else:
                print("El worker1, ha mandado este vector")
            for i in vector:
                print("\n"+vector[i])

    except Exception as ex:
        print(f'Error receiving the vector: {ex}')
    finally:
        client_socket.close()

def start_client() -> None:
    
    #Objeto de tipo cliente socket, que se utilizara para establecer la conexcion y enviar o recibir datos 
    client_socket0 = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    client_socket0.connect((SERVER_IP_ADDRESS_WORKER0,SERVER_PORT))
    print("conectado a worker0")
    
    client_socket1 = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    client_socket1.connect((SERVER_IP_ADDRESS_WORKER1,SERVER_PORT))
    print("conectado a worker1")

    receive_thread0 = th.Thread(target=receive_vector, args=(client_socket0,True,))
    receive_thread0.daemon = True
    receive_thread0.start()

    receive_thread1 = th.Thread(target=receive_vector, args=(client_socket0,False,))
    receive_thread1.daemon = True
    receive_thread1.start()

if __name__ == '__main__':
    start_client()


