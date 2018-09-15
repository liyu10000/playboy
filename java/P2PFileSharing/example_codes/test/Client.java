import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.lang.StringBuffer;
import java.net.Socket;

public class Client {
	Socket client;

	public void listen(String ip, int port) {
		try {
			client = new Socket(ip, port);
			System.out.println("Connected to server.");
			while (true) {
				// read cmdLine input from client
				System.out.print("> ");
				BufferedReader in = new BufferedReader(new InputStreamReader(System.in));
				String cmdLine = in.readLine();

				// send cmdLine to server
				PrintWriter out = new PrintWriter(client.getOutputStream(), true);
				out.println(cmdLine);

				// read cmdLine output from server
				BufferedReader serverOut = new BufferedReader(new InputStreamReader(client.getInputStream()));
				StringBuffer buffer = new StringBuffer();
				String serverLine = null;
				while ((serverLine = serverOut.readLine()) != null) {
					if (serverLine.equalsIgnoreCase("<<//file>>")) {
						break;
					}
					buffer.append(serverLine).append(System.getProperty("line.separator"));
				}
				System.out.println(buffer.toString());

				// check if cmdLine is "exit"
				if (cmdLine.equals("exit")) {
					client.close();
					in.close();
					out.close();
					serverOut.close();
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
		(new Client()).listen(args[0], Integer.valueOf(args[1]));
	}
}