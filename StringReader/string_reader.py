#Import libraries for socket communication, threading, and server_constants

import server_constants, socket, threading

#Define new socket connection object for the client
server_socket = socket.socket()
server_address = server_constants.SERVER_ADDRESS


#Start the server
def execute_server():
    server_port_tuple = (server_address, server_constants.SERVER_PORT)
    server_socket.bind(server_port_tuple)
    #Allow five unaccepted connections before refusing new connections
    server_socket.listen(5)
    print(f'Socket is listening on port {server_constants.SERVER_PORT}...')

    #Start handling client messages
    while True:
        client_connection, client_address = server_socket.accept()
        print(f'{client_address[0]} has connected on port {str(client_address[1])}')
        #Create a new thread to take care of each new client
        client_thread = threading.Thread(target=handle_client, args=(client_connection, client_address))
        client_thread.start()
    print('Closing socket...')
    server_socket.close()


#Functionality for handling client messages
def handle_client(connection, address):
    print("Handling client...")


def main():
    execute_server()



if __name__ == "__main__":
    main()