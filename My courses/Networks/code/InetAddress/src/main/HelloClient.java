package main;
import java.io.*;
import java.net.*;

public class HelloClient {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("What is your name?" );        
        try {
			try {
				String name = br.readLine();
				Socket socketClient = new Socket("localhost", 8000);
				BufferedReader readerClient = new BufferedReader(new InputStreamReader(socketClient.getInputStream()));
				PrintWriter writerClient =  new PrintWriter(socketClient.getOutputStream(), true);
				
				writerClient.println(name);
				System.out.println(readerClient.readLine());
				
				writerClient.close();
				readerClient.close();
				socketClient.close();
				
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			System.err.println("Invalid Format!");
		}
	}

}
