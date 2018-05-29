//package letschat;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

public class Client {  
  
    public static void main(String[] args) {  
        try {  
            Socket client = new Socket("127.0.0.1", 9999);  
            PrintWriter pw = null;  
            InputStreamReader isr = null;  
            System.out.println("Client started, ready to write content.");  
            String input = "";  
            while (true) {  
            	System.out.print("Client : ");  
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
                System.out.println(new BufferedReader(isr).readLine());  
            }  
            System.out.println("Client stopped!");  
        } catch (IOException e) {  
            // TODO Auto-generated catch block  
            e.printStackTrace();  
        }  
    }  
  
}  