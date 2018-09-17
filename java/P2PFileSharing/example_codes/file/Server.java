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

	public void sendFile(String filename) {
		try {
			Socket client = server.accept();
			System.out.println("Client connected.");
			
			File f = new File(filename);
			byte[] b = new byte[(int) f.length()];
			FileInputStream fis = new FileInputStream(f);
			BufferedInputStream bis = new BufferedInputStream(fis);
			bis.read(b, 0, b.length);
			DataOutputStream dos = new DataOutputStream(client.getOutputStream());
			dos.write(b, 0, b.length);
			dos.flush();
			System.out.println("Sent " + filename + " to client.");

			if (fis != null) fis.close();
			if (bis != null) bis.close();
			if (dos != null) dos.close();
			if (client != null) client.close();

			System.out.println("\nServer session ended.");
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	public static void main(String[] args) {
		(new Server(Integer.valueOf(args[0]))).sendFile(args[1]);
	}
}