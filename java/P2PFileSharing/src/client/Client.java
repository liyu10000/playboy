package client;

import java.io.IOException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.Socket;
import java.util.concurrent.TimeUnit;
import java.util.ArrayList;
import java.util.AbstractMap.SimpleEntry;

import util.Util;
import util.FileInfo;

public class Client {
	private String host;
	private int port;

	public Client(String host, int port) {
		this.host = host;
		this.port = port;
	}

	public ArrayList<SimpleEntry<String, FileInfo>> control() {
		ArrayList<SimpleEntry<String, FileInfo>> commands = new ArrayList<SimpleEntry<String, FileInfo>>();
		SimpleEntry<String, FileInfo> cmd1 = new SimpleEntry<>("client_to_server", new FileInfo("test.txt", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res", "C:/tsimage/playboy/java/P2PFileSharing/res", false));
		commands.add(cmd1);
		SimpleEntry<String, FileInfo> cmd2 = new SimpleEntry<>("server_to_client", null);
		commands.add(cmd2);
		SimpleEntry<String, FileInfo> cmd3 = new SimpleEntry<>("client_to_server", new FileInfo("test.xml", "/home/sakulaki/yolo-yuli/playboy/java/P2PFileSharing/res", "C:/tsimage/playboy/java/P2PFileSharing/res", false));
		commands.add(cmd3);
		SimpleEntry<String, FileInfo> cmd4 = new SimpleEntry<>("close", null);
		commands.add(cmd4);
		return commands;
	}

	public void run() throws Exception {
		Socket client = new Socket(host, port);
		System.out.println("Connected to server " + host + ":" + port);
		DataInputStream dis = new DataInputStream(client.getInputStream());
		DataOutputStream dos = new DataOutputStream(client.getOutputStream());

		ArrayList<SimpleEntry<String, FileInfo>> commands = control();
		for (SimpleEntry<String, FileInfo> command : commands) {
			String signal = command.getKey();
			FileInfo fileInfo = command.getValue();
			dos.writeUTF(signal);
			System.out.println("[SIGNAL] " + signal);
			switch(signal) {
				case "client_to_server":
					Util.push(client, dos, fileInfo, false);
					System.out.println("[INFO] sent file to server.");
					break;
				case "server_to_client":
					Util.pull(client, dis);
					System.out.println("[INFO] received file from server.");
					break;
			}
			TimeUnit.SECONDS.sleep(3);
		}

		client.close();
		System.out.println("\nClient session ended.");
	}

	public static void main(String[] args) throws Exception {
		(new Client(args[0], Integer.valueOf(args[1]))).run();
	}
}