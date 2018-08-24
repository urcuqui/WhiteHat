package main;
import java.io.*;
import java.net.*;

public class HelloServer {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		ServerSocket server = null;
		try 
		{
			// let's define the server socket in 8000
			server = new ServerSocket(8000);
			System.out.println("The server is running in..." +  server.getLocalPort());
			// the idea is to make a loop in order to receive different requests from the clients
			while(true)
			{				
				// now when the socket receive the answer from the client 
				Socket socket = server.accept();		
				System.out.println(socket.getInetAddress().getHostAddress());
				// now the we make the buffered and printwriter to the socket previously created ... these are the mechanisms to send and receive streams
				BufferedReader readerServer = new BufferedReader(new InputStreamReader(socket.getInputStream()));
				PrintWriter serverWriter = new PrintWriter(socket.getOutputStream());
				
				String name = readerServer.readLine();
				serverWriter.println("Hey!! " + name);
				
				// the next code lines are important 
				serverWriter.close();
				readerServer.close();
				socket.close();
			}			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
			try {
				server.close();
			} catch (IOException e1) {
				// TODO Auto-generated catch block
				e1.printStackTrace();
			}
		}		
	}
}
