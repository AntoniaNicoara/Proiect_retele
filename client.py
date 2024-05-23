import socket
import threading

def client_program(client_id, client_name, server_ip='127.0.0.1', server_port=5555):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((server_ip, server_port))
    
    client_socket.send(client_name.encode())  # Trimite numele clientului la conectare

    def receive_messages():
        while True:
            try:
                response = client_socket.recv(1024).decode()
                if response:
                    print(f"\nClient {client_id} - Server response: {response}")
                    if 'LOCK_ACQUIRED' in response or 'LOCK_RELEASED' in response:
                        print(f"Client {client_id} - Enter command (ACQUIRE/RELEASE) and semaphore name: ", end='', flush=True)
            except:
                break
    
    threading.Thread(target=receive_messages, daemon=True).start()
    
    print(f"Client {client_id} - Enter command (ACQUIRE/RELEASE) and semaphore name: ", end='', flush=True)
    while True:
        command = input()
        if command.lower() == 'exit':
            break
        client_socket.send(command.encode())
    
    client_socket.close()

if __name__ == "__main__":
    import sys
    client_id = int(sys.argv[1])
    client_name = input(f"Enter name for client {client_id}: ")
    client_program(client_id, client_name)
