#Import libraries for socket communicaton and constants

import socket, client_constants

#Define new socket connection object for the client
client_socket = socket.socket()


#Start the client
def execute_client():
    client_port_tuple = (client_constants.CLIENT_ADDRESS, client_constants.PORT)
    client_socket.connect(client_port_tuple)
    local_tuple = client_socket.getsockname()
    print(local_tuple)


#Handle client prompts and commands
def handle_inputs():
    pass


def main():
    execute_client()


if __name__ == '__main__':
    main()