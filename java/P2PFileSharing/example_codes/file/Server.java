import java.io.File;
import java.io.IOException;
import java.io.FileInputStream;
import java.io.BufferedInputStream;
import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	private ServerSocket server;
	
	public Server(int port) {
		try {
			server = new ServerSocket(port);
			System.out.println("Server started at port: " + port);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public void sendHead(Socket socket, String directory, String filename, long length) throws IOException {
		DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
		
		// start
		dos.writeByte(0);
		dos.flush();
		// directory
		dos.writeByte(1);
		dos.writeUTF(directory);
		dos.flush();
		// filename
		dos.writeByte(2);
		dos.writeUTF(filename);
		dos.flush();
		// file length
		dos.writeByte(3);
		dos.writeInt((int)length);
		dos.flush();
		// end
		dos.writeByte(-1);
		dos.flush();

		dos.close();

		System.out.println("head sent.");
	}

	public void sendBody(Socket socket, String filename) throws IOException {
		File f = new File(filename);
		byte[] b = new byte[(int) f.length()];
		FileInputStream fis = new FileInputStream(f);
		BufferedInputStream bis = new BufferedInputStream(fis);
		bis.read(b, 0, b.length);
		DataOutputStream dos = new DataOutputStream(socket.getOutputStream());
		dos.write(b, 0, b.length);
		dos.flush();
	
		fis.close();
		bis.close();
		dos.close();
		
		System.out.println("body sent.");
	}

	public void send(String filename) throws IOException {
		Socket client = server.accept();
		System.out.println("Client connected.");

		File f = new File(filename);
		sendHead(client, "/home", filename, f.length());
		sendBody(client, filename);

		client.close();
		System.out.println("\nServer session ended.");
	}

	public static void main(String[] args) throws IOException {
		(new Server(Integer.valueOf(args[0]))).send(args[1]);
	}
}