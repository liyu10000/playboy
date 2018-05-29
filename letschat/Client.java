public class Client {  
  
    public static void main(String[] args) {  
        try {  
            Socket client = new Socket("127.0.0.1", 9999);  
            PrintWriter pw = null;  
            InputStreamReader isr = null;  
            Helper.println("Client started, ready to write content.");  
            String input = "";  
            while (true) {  
                Helper.print("Client : ");  
                InputStream is = System.in;  
                input = new BufferedReader(new InputStreamReader(is))  
                        .readLine();  
                pw = new PrintWriter(client.getOutputStream(), true);  
                pw.println("Client:" + input);  
                if (input.equals("end")) {  
                    client.close();  
                    is.close();  
                    pw.close();  
                    if (isr != null) {  
                        isr.close();  
                    }  
                    break;  
                }  
                isr = new InputStreamReader(client.getInputStream());  
                Helper.println(new BufferedReader(isr).readLine());  
            }  
            Helper.println("Client stopped!");  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
  
}  