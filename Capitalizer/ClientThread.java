package Capitalizer;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.net.Socket;

public class ClientThread extends Thread {
    private Socket clientSocket;
    private String encodingFormat;

    public ClientThread(Socket clientSocket, String encodingFormat) {
        this.clientSocket = clientSocket;
        this.encodingFormat = encodingFormat;
    }

    public void run() {
        try {
            // Object to read client input
            InputStream inputStream = clientSocket.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream, encodingFormat));

            // Output stream
            OutputStreamWriter outputStreamWriter = new OutputStreamWriter(clientSocket.getOutputStream(),
                    encodingFormat);
            // Output stream to socket and flush buffer
            PrintWriter printWriter = new PrintWriter(outputStreamWriter, true);

            String clientText = "";

            do {
                clientText = bufferedReader.readLine();
                String allCapsText = clientText.toUpperCase();

                // If the client isn't quitting, print message
                if (!clientText.equals("0")) {
                    // Print client text
                    System.out.println("The original message was: " + clientText);
                    // Print modified text
                    System.out.println("The capitalized message is: " + allCapsText);
                    // Write response through socket
                    printWriter.println("40 - MSG OK -> TRANSFERRING TO REVERSER");
                }
            } while (!clientText.equals("0"));

            System.out.println("Client with address " + clientSocket.getInetAddress().toString() + " on port "
                    + clientSocket.getPort() + " disconnected\n");

            // Send exit response to Reader
            printWriter.println("10 - QUIT\n");
            clientSocket.close();

        } catch (IOException ex) {
            System.out.println("Server exception: " + ex.getLocalizedMessage());
        }
    }
}
