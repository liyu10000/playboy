
public class Main {
	public static void main(String[] args) {
		Logger log = new Logger("./log.txt");
		log.log("This is a line.");
		log.log("This is another line.");
		System.out.println("done.");
	}
}