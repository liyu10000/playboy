package server;

import java.io.IOException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.TimeUnit;

import util.Util;
import util.FileInfo;

public class Server {
	private int port;

	public Server(int port) {
		this.port = port;
	}

	public void control() throws Exception {
		ServerSocket server = new ServerSocket(port);
		System.out.println("Server started at port: " + port);
		Socket client = server.accept();
		System.out.println("Client connected.");

		DataInputStream dis = new DataInputStream(client.getInputStream());
		DataOutputStream dos = new DataOutputStream(client.getOutputStream());
		String[] signals = new String[]{"server_to_client", "client_to_server", "server_to_client", "close"};
		for (String signal : signals) {
			dos.writeUTF(signal);
			System.out.println("[SIGNAL] " + signal);
			switch(signal) {
				case "client_to_server":
					// Util.pull(client, dis);
					// System.out.println("[INFO] received file from client.");
					break;
				case "server_to_client":
					FileInfo fileInfo = new FileInfo("test.xml", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res", "C:/tsimage/playboy/java/P2PFileSharing/res", true);
					Util.push(client, dos, fileInfo, true);
					System.out.println("[INFO] sent file to client.");
					break;
			}
			TimeUnit.SECONDS.sleep(3);
		}

		client.close();
		server.close();
		System.out.println("\nServer session ended.");
	}

	public static void main(String[] args) throws Exception {
		(new Server(Integer.valueOf(args[0]))).control();
	}
}