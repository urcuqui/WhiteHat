package multiThreadsSC;
import java.io.*;
import java.net.*;
import java.util.Scanner;

public class WelcomeClient {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		Socket client;
		BufferedReader readerC;
		PrintWriter writerC;
		String name, answer, host;
		int port;
		Scanner scanner = new Scanner(System.in);
		//  we are going to make the socket and the streams associated
		try
		{
			client = new Socket("localhost", 8030);
			readerC =  new BufferedReader(new InputStreamReader(client.getInputStream()));
			writerC =  new PrintWriter(client.getOutputStream(), true);
			
			// we are going to get the user name and his host
			host = client.getLocalAddress().getHostName();
			port = client.getLocalPort();
			System.out.println("Write your name");
			name = scanner.nextLine();
			
			/* The server port is going to show in the screen to verify that 
			 * it is the same in the server
			 */
			System.out.println(port);
			
			// The data is going to send to the server
			writerC.println(name);
			writerC.println(host + ("( port: " +port+")"));
			
			// The server answer is going to process
			answer = readerC.readLine();
			System.out.println(answer);
			
			// We are going to close the streams and sockets
			readerC.close();
			writerC.close();
			client.close();
			
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

}
