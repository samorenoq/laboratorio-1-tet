# Import libraries for socket communication, threading, and server_constants

import server_constants
import socket
import threading

# Define new socket connection object for the client
server_socket = socket.socket()
server_address = server_constants.SERVER_ADDRESS
encoding = server_constants.ENCODING_FORMAT
port = server_constants.SERVER_PORT
buff_size = server_constants.RECV_BUFFER_SIZE


# Start the server
def execute_server():
    server_port_tuple = (server_address, port)
    server_socket.bind(server_port_tuple)
    # Allow five unaccepted connections before refusing new connections
    server_socket.listen(5)
    print(f'Socket is listening on port {port}...')

    # Start handling client messages
    while True:
        client_connection, client_address = server_socket.accept()
        print(
            f'{client_address[0]} has connected using their port {str(client_address[1])}')
        # Create a new thread to take care of each new client
        client_thread = threading.Thread(
            target=handle_client, args=(client_connection, client_address))
        client_thread.start()
    print('Closing socket...')
    server_socket.close()


# Functionality for handling client messages
def handle_client(client_connection: socket.socket, client_address: tuple) -> None:
    client_is_connected = True

    while client_is_connected:
        client_message = str(client_connection.recv(
            buff_size).decode(encoding))

        # If the client wants to exit
        if client_message == str(server_constants.EXIT):
            response = '10 - QUIT\n'
            client_connection.sendall(response.encode(
                encoding
            ))
            client_is_connected = False

        # If the client's message contains invalid characters
        elif not client_message.isalpha():
            response = '20 - INVALID CHARACTERS\n'
            send_to_client(client_connection, response)

        # Otherwise, the client's message is ok
        else:
            response = '30 - MSG OK -> TRANSFERRING'
            send_to_client(client_connection, response)

    print(
        f'Client with address {client_address[0]} on port {client_address[1]} disconnected')
    client_connection.close()


# Function to define behavior for sending messages to the client
def send_to_client(client_connection: socket.socket, msg: str) -> None:
    client_connection.sendall(msg.encode(encoding))


def main():
    execute_server()


if __name__ == "__main__":
    main()
