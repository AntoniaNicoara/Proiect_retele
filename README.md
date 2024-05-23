### README

# Remote Process Synchronization Project

This project consists of a client-server application developed in Python. The project ensures remote process synchronization through semaphores managed by the server. Clients can connect to the server, request exclusive access to semaphores, and release the semaphores after use.

## Features

1. **Remote Process Synchronization**:
    - The server ensures the synchronization of processes executing in client applications through semaphores.
    - Clients connect to the server and maintain an open connection during the execution of the client process.

2. **Exclusive Semaphore Access**:
    - A client can request exclusive access to a semaphore identified by a unique name on the server.
    - If no other client has exclusive access to that semaphore, the server grants the client access, noting which client accesses the semaphore.
    - If a client already has access to that semaphore, the server will deny the new client's request for exclusive access, adding the new client to a waiting list for that semaphore.

3. **Semaphore Release**:
    - When the client holding exclusive access to a semaphore releases it, the server will grant exclusive access to the next client in the waiting list, if any, notifying them accordingly.

## Requirements Fulfilled

1. **Concurrent Server**:
    - The server allows subscription and notification of clients according to the functional requirements.

2. **Capable Client**:
    - The client can subscribe, invoke the server, and handle callbacks from the server.

## Installation and Usage Instructions

### Prerequisites

Ensure you have Python installed on your system. To verify, run the following command in the terminal:

```sh
python --version
```

### Installation

1. Clone this repository or download the necessary files.
2. Ensure you have the following files:
    - `server.py`
    - `client.py`

### Usage

1. **Start the Server**:

   In a terminal window, navigate to the directory containing the files and run:

   ```sh
   python server.py
   ```

   The server will start listening for connections on port 5555.

2. **Start the Clients**:

   In other terminal windows, run multiple instances of the client using the following command:

   ```sh
   python client.py 1
   ```

   For each client, enter a unique name when prompted and then use the `ACQUIRE` and `RELEASE` commands followed by the semaphore name to request and release access to semaphores.

### Example Usage

1. **Client 1**:

   ```sh
   Client 1 - Enter command (ACQUIRE/RELEASE) and semaphore name: ACQUIRE test_semaphore
   Client 1 - Server response: LOCK_ACQUIRED test_semaphore
   Client 1 acquired the semaphore.
   ```

2. **Client 2**:

   ```sh
   Client 2 - Enter command (ACQUIRE/RELEASE) and semaphore name: ACQUIRE test_semaphore
   Client 2 - Server response: WAIT test_semaphore
   ```

3. **Client 1 Releases the Semaphore**:

   ```sh
   Client 1 - Enter command (ACQUIRE/RELEASE) and semaphore name: RELEASE test_semaphore
   Client 1 - Server response: LOCK_RELEASED test_semaphore
   Client 1 released the semaphore.
   ```

4. **Client 2 Acquires the Semaphore**:

   ```sh
   Client 2 - Server response: LOCK_ACQUIRED test_semaphore
   Client 2 acquired the semaphore.
   ```

### Notifications

When a client releases a semaphore, all other clients will receive a message in the terminal as follows:

```sh
Client [Name] ([IP], [Port]) released semaphore [SemaphoreName]
```

This ensures that all clients are notified about the semaphore release and can act accordingly.

---

This is an educational project aimed at demonstrating the use of semaphores for remote process synchronization using Python.
