import java.io.IOException;
import java.io.FileOutputStream;
import java.io.DataInputStream;
import java.net.Socket;

public class Client {
	private String host;
	private int port;

	public Client(String host, int port) {
		this.host = host;
		this.port = port;
	}

	public void save(Socket socket, DataInputStream dis) throws IOException {
		String directory = dis.readUTF();
		String filename = dis.readUTF();
		int length = dis.readInt();
		// System.out.println("[INFO] head saved.");

		FileOutputStream fos = new FileOutputStream(filename);
		byte[] b = new byte[4096];
		int filesize = length;
		int read = 0;
		int totalRead = 0;
		int remaining = filesize;
		while ((read = dis.read(b, 0, Math.min(b.length, remaining))) > 0) {
			totalRead += read;
			remaining -= read;
			fos.write(b, 0, read);
		}
		fos.close();
		// System.out.println("[INFO] body saved.");

		System.out.println("[INFO] received " + filename + " from server.");
	}

	public void control() throws IOException {
		Socket client = new Socket(host, port);
		System.out.println("Connected to server " + host + ":" + port);
		DataInputStream dis = new DataInputStream(client.getInputStream());
		while (true) {
			String signal = dis.readUTF();
			System.out.println("[SIGNAL] " + signal);
			switch(signal) {
				case "client_to_server":
					break;
				case "server_to_client":
					save(client, dis);
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