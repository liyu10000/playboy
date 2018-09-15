import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {
	Socket client;

	public void listen(String ip, int port) {
		try {
			client = new Socket(ip, port);
			System.out.println("Connected to server.");
			BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
			PrintWriter out = new PrintWriter(client.getOutputStream(), true);;
			while (true) {
				System.out.print("> ");
				String line = in.readLine();
				out.println(line);
				if (line.equals("exit") || line.equals("quit")) {
					client.close();
					in.close();
					out.close();
					break;
				}
			}
			System.out.println("\nServer offline! Client Closed.");
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	public static void main(String[] args) {
		(new Client()).listen("127.0.0.1", 9999);
	}
}