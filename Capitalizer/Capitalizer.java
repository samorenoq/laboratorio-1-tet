package Capitalizer;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

/**
 * This program receives a string from a socket and turns it into all caps.
 * Example: Input: "Hello World" Output: "HELLO WORLD"
 * 
 * @author Santiago Moreno
 */
public class Capitalizer {
    public static final int port = 50001;
    public static final String encodingFormat = "UTF-8";

    public static void main(String[] args) {
        try {
            // Create a new server socket on port 50001
            ServerSocket serverSocket = new ServerSocket(port);
            System.out.println("Capitalizer is listening on port " + port + "\n");

            // Accept new connections
            while (true) {
                // New client connections
                Socket clientSocket = serverSocket.accept();
                System.out.println(clientSocket.getInetAddress().toString() + " connected on their port "
                        + clientSocket.getPort() + "\n");

                //Create new thread to handle client
                new ClientThread(clientSocket, encodingFormat).start();
            }

        } catch (IOException ex) {
            System.out.println("Server exception: " + ex.getLocalizedMessage());
        }
    }
}