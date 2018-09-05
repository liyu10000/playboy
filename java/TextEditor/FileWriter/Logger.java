import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Date;

public class Logger {
	private File logFile;

	public Logger() {}

	public Logger(String name) {
		logFile = new File(name);
	}

	public Logger(File f) {
		logFile = f;
	}

	public void log(String s) {
		try {
			FileWriter fw = new FileWriter(this.logFile, true);
			String date = new Date().toString();
			String info = date + ": " + s;
			fw.write(info);
			fw.write(System.lineSeparator());
			fw.close();
		} catch (IOException e) {
			System.err.println("[ERROR] could not log this: " + s);
		}
	}

}

