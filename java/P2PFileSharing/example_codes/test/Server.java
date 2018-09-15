import java.io.File;
import java.io.IOException;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.lang.Process;
import java.lang.ProcessBuilder;
import java.lang.StringBuffer;
import java.net.ServerSocket;
import java.net.Socket;

public class Server {
	ServerSocket server;
	Socket client;

	private void listen(int port) {
		try {
			server = new ServerSocket(port);
			System.out.println("Server started.");
			client = server.accept();
			System.out.println("Client connected.");
			while (true) {
				// read cmdLine from client
				System.out.print("> ");
				BufferedReader in = new BufferedReader(new InputStreamReader(client.getInputStream()));
				String cmdLine = in.readLine();
				System.out.println(cmdLine);

				// execute cmdLine and get output
				String cmdOutput = command(cmdLine, System.getProperty("user.home"));
				System.out.println(cmdOutput.substring(0, cmdOutput.length()-10));

				// send cmdLine output to client
				PrintWriter out = new PrintWriter(client.getOutputStream(), true);
				out.println(cmdOutput);

				// check if cmdLine is "exit"
				if (cmdLine.equals("exit")) {
					server.close();
					in.close();
					out.close();
					break;
				}
			}
			System.out.println("\nClient left! Server Closed.");
		} catch (IOException e) {
			e.printStackTrace();
			System.exit(-1);
		}
	}

	private String command(final String cmdLine, final String directory) {
		String result = null;
		try {
			ProcessBuilder builder = new ProcessBuilder();
			if (System.getProperty("os.name").toLowerCase().startsWith("windows")) {
				builder.command(new String[] {"cmd.exe", "/c", cmdLine});
			} else {
				builder.command(new String[] {"bash", "-c", cmdLine});
			}
			builder.redirectErrorStream(true);
			builder.directory(new File(directory));
			Process process = builder.start();
			StringBuffer out = new StringBuffer();
			BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()));
			String line = null;
			while ((line = br.readLine()) != null) {
				out.append(line).append(System.getProperty("line.separator"));
			}

			result = out.toString();

			if (0 != process.waitFor()) {
				result = "command line cannot be executed"
					   	 + System.getProperty("line.separator");
			}
		} catch (Exception e) {
			StringWriter sw = new StringWriter();
			PrintWriter pw = new PrintWriter(sw);
			e.printStackTrace(pw);
			result = sw.toString();
			pw.close();
			// sw.close();
		}
		return result + "<<//file>>";
	} 

	public static void main(String[] args) {
		(new Server()).listen(Integer.valueOf(args[0]));
	}
}