package main;
import java.net.*;
import java.io.*;
public class Email {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		//SMTP service from gmail smtp-relay.gmail.com
		// to use gmail is necessary to use security mechanisms in order to log with an email account 
		try {
			Socket socket =  new Socket("smtp-relay.gmail.com", 25);
			BufferedReader reader = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			PrintStream writer = new PrintStream(socket.getOutputStream());
			writer.println("mail from: ...@gmail.com");
			System.out.println(reader.readLine());
			
			String address = "...@gmail.com";
			writer.println("rcpt to:" + address);
			
			System.out.println(reader.readLine());
			
			writer.println("data");
			System.out.println(reader.readLine());
			
			writer.println("This is the message \n that Java sent");
			writer.println(".");
			System.out.println(reader.readLine());
			
			writer.flush();
			socket.close();
			writer.close();
			reader.close();
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
