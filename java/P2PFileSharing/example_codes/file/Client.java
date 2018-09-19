import java.io.IOException;
import java.io.FileOutputStream;
import java.io.DataInputStream;
import java.net.Socket;

public class Client {
	private Socket client;
	String directory;
	String filename;
	int length;


	public Client(String host, int port) {
		try {
			client = new Socket(host, port);
			System.out.println("Connected to server " + host + ":" + port);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void _save(Socket socket) throws IOException {
		DataInputStream dis = new DataInputStream(socket.getInputStream());
		byte signal = dis.readByte();
		while (signal != -1) {
			signal = dis.readByte();
			switch(signal) {
				case 1:
					directory = dis.readUTF();
					break;
				case 2:
					filename = dis.readUTF();
					break;
				case 3:
					length = dis.readInt();
					break;
				default:
					signal = -1;
			}
		}
		// dis.close();
		System.out.println("head saved. filename: " + filename);

		// DataInputStream dis = new DataInputStream(socket.getInputStream());
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
		dis.close();
		System.out.println("body saved.");
	}

	public void save() throws IOException {
		_save(client);
		System.out.println("Read " + filename + " from server.");
		client.close();
		System.out.println("\nClient session ended.");
	}

	public static void main(String[] args) throws IOException {
		(new Client(args[0], Integer.valueOf(args[1]))).save();
	}
}