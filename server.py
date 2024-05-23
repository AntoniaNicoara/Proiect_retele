import socket
import threading

semaphores = {}
semaphores_locks = threading.Lock()
clients = {}
clients_lock = threading.Lock()

def handle_client(client_socket, client_address):
    client_name = client_socket.recv(1024).decode() 
    with clients_lock:
        clients[client_socket] = (client_name, client_address)
    
    try:
        while True:
            request = client_socket.recv(1024).decode()
            if not request:
                break
            
            command, semaphore_name = request.split()
            
            with semaphores_locks:
                if command == 'ACQUIRE':
                    if semaphore_name not in semaphores:
                        semaphores[semaphore_name] = {
                            'owner': client_socket,
                            'waiting_list': []
                        }
                        response = f'LOCK_ACQUIRED {semaphore_name}'
                        print(f"{client_name} ({client_address}) acquired {semaphore_name} (no prior owner).")
                    elif semaphores[semaphore_name]['owner'] is None:
                        semaphores[semaphore_name]['owner'] = client_socket
                        response = f'LOCK_ACQUIRED {semaphore_name}'
                        print(f"{client_name} acquired {semaphore_name} (was released).")
                    else:
                        semaphores[semaphore_name]['waiting_list'].append(client_socket)
                        response = f'WAIT {semaphore_name}'
                        print(f"{client_name} is waiting for {semaphore_name}. Current owner: {clients[semaphores[semaphore_name]["owner"]][0]}.")
                
                elif command == 'RELEASE':
                    if semaphore_name in semaphores and semaphores[semaphore_name]['owner'] == client_socket:
                        notify_all_clients(f"Client {client_name} released semaphore {semaphore_name}")
                        if semaphores[semaphore_name]['waiting_list']:
                            next_client = semaphores[semaphore_name]['waiting_list'].pop(0)
                            semaphores[semaphore_name]['owner'] = next_client
                            next_client.send(f'LOCK_ACQUIRED {semaphore_name}'.encode())
                            print(f"{client_name} released {semaphore_name}. Next client: {clients[next_client][0]}.")
                        else:
                            semaphores[semaphore_name]['owner'] = None
                            print(f"{client_name} released {semaphore_name}. No clients waiting.")
                        response = f'LOCK_RELEASED {semaphore_name}'
                    else:
                        response = f'LOCK_NOT_OWNED {semaphore_name}'
                else:
                    response = 'UNKNOWN_COMMAND'
            
            client_socket.send(response.encode())
    except ConnectionResetError:
        pass
    finally:
        with clients_lock:
            del clients[client_socket]
        client_socket.close()

def notify_all_clients(message):
    with clients_lock:
        for client in clients:
            try:
                client.send(message.encode())
            except:
                clients.pop(client, None)

def start_server(port=5555):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', port))
    server_socket.listen(5)
    print(f'Server started on port {port}')
    
    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Accepted connection from {client_address}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_handler.start()

if __name__ == "__main__":
    start_server()
