package client;

import java.io.IOException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;

import util.Util;
import util.FileInfo;

public class Client {
	private String host;
	private int port;

	public Client(String host, int port) {
		this.host = host;
		this.port = port;
	}

	public void control() throws IOException {
		Socket client = new Socket(host, port);
		System.out.println("Connected to server " + host + ":" + port);
		DataInputStream dis = new DataInputStream(client.getInputStream());
		DataOutputStream dos = new DataOutputStream(client.getOutputStream());
		while (true) {
			String signal = dis.readUTF();
			System.out.println("[SIGNAL] " + signal);
			switch(signal) {
				case "client_to_server":
					// FileInfo fileInfo = new FileInfo("test2.jpg", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res", "C:/tsimage/playboy/java/P2PFileSharing/res", false);
					// Util.push(client, dos, fileInfo, false);
					// System.out.println("[INFO] sent file to server.");
					break;
				case "server_to_client":
					Util.pull(client, dis);
					System.out.println("[INFO] received file from server.");
					break;
			}
			if (signal.equals("close")) {
				break;
			}
		}
		client.close();
		System.out.println("\nClient session ended.");
	}

	public static void main(String[] args) throws IOException {
		(new Client(args[0], Integer.valueOf(args[1]))).control();
	}
}