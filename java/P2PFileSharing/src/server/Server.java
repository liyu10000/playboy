package server;

import java.io.IOException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

import util.Util;
import util.FileInfo;

public class Server {
	private int port;

	public Server(int port) {
		this.port = port;
	}

	public void run() throws IOException {
		ServerSocket server = new ServerSocket(port);
		System.out.println("Server started at port: " + port);
		Socket client = server.accept();
		System.out.println("Client connected.");

		DataInputStream dis = new DataInputStream(client.getInputStream());
		DataOutputStream dos = new DataOutputStream(client.getOutputStream());

		while (true) {
			String signal = dis.readUTF();
			System.out.println("[SIGNAL] " + signal);
			switch(signal) {
				case "client_to_server":
					Util.pull(client, dis);
					System.out.println("[INFO] received file from client.");
					break;
				case "server_to_client":
					String[] twoFilenames = Util.pullInfo(client, dis);
					FileInfo fileInfo = new FileInfo(twoFilenames[0], twoFilenames[1], true);
					Util.push(client, dos, fileInfo);
					System.out.println("[INFO] sent file to client.");
					break;
			}
			if (signal.equals("close")) {
				break;
			}
		}

		client.close();
		server.close();
		System.out.println("\nServer session ended.");
	}

	public static void main(String[] args) throws IOException {
		(new Server(Integer.valueOf(args[0]))).run();
	}
}