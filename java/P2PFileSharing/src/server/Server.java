package server;

import java.io.IOException;
import java.io.EOFException;
import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;

import util.Util;
import util.FileInfo;

public class Server {
	private int port;
	private ServerSocket server;
	private Socket client;
	private DataInputStream dis;
	private DataOutputStream dos;

	public Server(int port) {
		this.port = port;
	}

	public void start() {
		try {
			server = new ServerSocket(port);
			System.out.println("[INFO  ] Server started at port: " + port);
		} catch (IOException e) {
			// e.printStackTrace();
			System.err.println("[ERROR ] cannot start server.");
		}
	}

	private void connect() {
		try {
			client = server.accept();
			System.out.println("\n[INFO  ] Client connected.");
			dis = new DataInputStream(client.getInputStream());
			dos = new DataOutputStream(client.getOutputStream());
		} catch (IOException e) {
			// e.printStackTrace();
			System.err.println("\n[ERROR ] client failed to connect with server.");
		}
	}

	public void shuttle() {
		connect();
		while (true) {
			try {
				String signal = dis.readUTF();
				System.out.println("[SIGNAL] " + signal);
				switch(signal) {
					case "client_to_server":
						Util.pull(client, dis);
						break;
					case "server_to_client":
						String[] twoFileNames = Util.pullInfo(client, dis);
						FileInfo fileInfo = new FileInfo(twoFileNames[0], twoFileNames[1], true);
						Util.push(client, dos, fileInfo);
						break;
				}
			} catch (NullPointerException e) {
				// e.printStackTrace();
				System.err.println("[ERROR ] pulling file info failed.");
			} catch (SocketException e) {
				// e.printStackTrace();
				System.err.println("[ERROR ] connection from client interrupted.");
				connect();
			} catch (EOFException e) {
				System.out.println("[INFO  ] connection from client closed.");
				connect();
			} catch (IOException e) {
				System.err.println("[ERROR ] undetermined error.");
				// e.printStackTrace();
			}
		}
	}

	public void close() {
		try {
			client.close();
			server.close();
			System.out.println("\n[INFO  ] Server session ended.");
		} catch (IOException e) {
			// e.printStackTrace();
			System.err.println("\n[ERROR ] failed to close connection.");
		}
	}

	public static void main(String[] args) {
		Server serverCase = new Server(Integer.valueOf(args[0]));
		serverCase.start();
		serverCase.shuttle();
	}

	/* used in commond line test
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
					String[] twoFileNames = Util.pullInfo(client, dis);
					FileInfo fileInfo = new FileInfo(twoFileNames[0], twoFileNames[1], true);
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
	*/
}