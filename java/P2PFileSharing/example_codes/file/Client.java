import java.io.IOException;
import java.io.FileOutputStream;
import java.io.DataInputStream;
import java.net.Socket;

public class Client {
	private Socket client;

	public Client(String host, int port) {
		try {
			client = new Socket(host, port);
			System.out.println("Connected to server " + host + ":" + port);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void saveFile(String filename) {
		try {
			DataInputStream dis = new DataInputStream(client.getInputStream());
			FileOutputStream fos = new FileOutputStream(filename);

			byte[] b = new byte[4096];
			int filesize = 1024000;
			int read = 0;
			int totalRead = 0;
			int remaining = filesize;
			while ((read = dis.read(b, 0, Math.min(b.length, remaining))) > 0) {
				totalRead += read;
				remaining -= read;
				fos.write(b, 0, read);
			}
			System.out.println("Read " + filename + " from server.");
			if (fos != null) fos.close();
			if (dis != null) dis.close();

			System.out.println("\nClient session ended.");
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	public static void main(String[] args) {
		(new Client(args[0], Integer.valueOf(args[1]))).saveFile(args[2]);
	}
}