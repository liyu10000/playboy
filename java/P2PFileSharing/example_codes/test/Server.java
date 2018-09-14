import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	ServerSocket server;
	Socket client;

	listen(int port) {
		try {
			server = new ServerSocket(port);
			client = server.accept();
			System.out.println("Server started, waiting for message.");
			PrintWriter out = null;
			while (true) {
				BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
				String line = in.readLine();
				if (line.equals("exit") || line.equals("quit")) {
					in.close();
					server.close();
					if (out != null) {
						out.close();
					}
					break;
				}
				System.out.println(line);
                System.out.print("Server:");
                BufferedReader serverIn = new BufferedReader(new InputStreamReader(System.in));
                String output = "Server : " + serverIn.readLine();
                out = new PrintWriter(client.getOutputStream(), true)
                out.println(output);
			}
			System.out.println("Client left! Server Closed.");
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	public static void main(String[] args) {
		new Server(9999);
	}
}