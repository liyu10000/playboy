import java.io.File;
import java.io.IOException;
import java.io.FileInputStream;
import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.concurrent.TimeUnit;

public class Server {
	private int port;

	public Server(int port) {
		this.port = port;
	}

	public void send(Socket socket, DataOutputStream dos, String filename) throws IOException {
		File file = new File(filename);
		// DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
		
		// directory
		dos.writeUTF("/home");
		dos.flush();
		// filename
		dos.writeUTF(filename);
		dos.flush();
		// file length
		dos.writeInt((int)file.length());
		dos.flush();
		// System.out.println("[INFO] head sent.");


		byte[] b = new byte[(int)file.length()];
		FileInputStream fis = new FileInputStream(file);
		BufferedInputStream bis = new BufferedInputStream(fis);
		bis.read(b, 0, b.length);
		dos.write(b, 0, b.length);
		dos.flush();
	
		fis.close();
		bis.close();
		// dos.close();
		
		// System.out.println("[INFO] body sent.");
		System.out.println("[INFO] sent " + filename + " to client.");
	}


	public void control() throws Exception {
		ServerSocket server = new ServerSocket(port);
		System.out.println("Server started at port: " + port);
		Socket client = server.accept();
		System.out.println("Client connected.");

		DataOutputStream dos = new DataOutputStream(client.getOutputStream());
		String[] signals = new String[]{"server_to_client", "client_to_server", "server_to_client", "close"};
		for (String signal : signals) {
			dos.writeUTF(signal);
			System.out.println("[SIGNAL] " + signal);
			switch(signal) {
				case "client_to_server":
					break;
				case "server_to_client":
					send(client, dos, "../../res/test.txt");
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