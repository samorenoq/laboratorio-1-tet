# Import libraries for socket communicaton and constants

import socket
import client_constants

# Define new socket connection object for the client
client_socket = socket.socket()

# Define constant variables
encoding = client_constants.ENCODING_FORMAT
buff_size = client_constants.RECV_BUFFER_SIZE

# Start the client


def execute_client():
    # This tuple contains the server port
    server_tuple = (client_constants.SERVER_ADDRESS,
                    client_constants.SERVER_PORT)
    client_socket.connect(server_tuple)
    # This tuple contains the client port
    client_connection_tuple = client_socket.getsockname()
    print(
        f'Connected to server on address {client_connection_tuple[0]} from port {client_connection_tuple[1]}\n')

    # Handle user inputs
    handle_inputs()


# Handle client prompts and commands
def handle_inputs():
    message_prompt = "Enter a message (a-z or A-Z only) or press '0' to exit: "
    message = ''
    while message != str(client_constants.EXIT):
        message = input(message_prompt)

        # Check that message is not empty
        if message == '':
            print('Empty message! Please try again...\n')
        else:
            client_socket.send(bytes(message, encoding))

            print('______________________________________')

            # Get the response from the reader
            response = client_socket.recv(buff_size)
            print(
                f'\nReader response: {response.decode(encoding)}\n')

            # Get the response from the capitalizer, sent by the reader
            capitalizer_response = client_socket.recv(buff_size)
            if (capitalizer_response):
                print(f'Capitalizer response: {capitalizer_response.decode(encoding)}')
            
            # Get the response from the reverser, sent by the reader
            reverser_response = client_socket.recv(buff_size)
            if (reverser_response):
                print(f'Reverser response: {reverser_response.decode(encoding).strip()}')

            print('______________________________________\n')

    # If the user exits the program
    print('Exiting...')
    client_socket.close()


def main():
    execute_client()


if __name__ == '__main__':
    main()
