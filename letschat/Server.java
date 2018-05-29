public class Server {  
  
    public static void main(String[] args) {  
        try {  
            ServerSocket server = new ServerSocket(9999);  
            Helper.println("Server started, waiting for message.");  
            Socket client = server.accept();  
            PrintWriter pw = null;  
            while (true) {  
                BufferedReader br = new BufferedReader(new InputStreamReader(  
                        client.getInputStream()));  
                String content = br.readLine();  
                if (content.equals("end")) {  
                    server.close();  
                    br.close();  
                    if (pw != null) {  
                        pw.close();  
                    }  
                    break;  
                }  
                Helper.println(content);  
                Helper.print("Server:");  
                pw = new PrintWriter(client.getOutputStream(), true);  
                BufferedReader in = new BufferedReader(new InputStreamReader(System.in));  
                String output = "Server : " + in.readLine();  
                pw.println(output);  
                pw.flush();  
            }  
            Helper.println("Client left! Server Closed.");  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
}  