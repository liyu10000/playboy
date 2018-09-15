import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	ServerSocket server;
	Socket client;

	public void listen(int port) {
		try {
			server = new ServerSocket(port);
			System.out.println("Server started.");
			client = server.accept();
			System.out.println("Client connected.");
			BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
			while (true) {
				System.out.print("> ");
				String line = in.readLine();
				System.out.println(line);
				if (line.equals("exit") || line.equals("quit")) {
					server.close();
					in.close();
					break;
				}
			}
			System.out.println("\nClient left! Server Closed.");
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	public static void main(String[] args) {
		(new Server()).listen(9999);
	}
}