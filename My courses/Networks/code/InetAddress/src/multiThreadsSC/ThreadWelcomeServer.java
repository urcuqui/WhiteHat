package multiThreadsSC;
import java.net.*;
import java.io.*;
public class ThreadWelcomeServer extends Thread{
	Socket client;
	BufferedReader readerHS;
	PrintWriter writerHS;
	
	public ThreadWelcomeServer(Socket request)
	{
		super();
		client = request;
	}
	/*
	 * (non-Javadoc)
	 * @see java.lang.Thread#run()
	 * Pay attention that the next method "run" has the business logic of the server 
	 */
	public void run()
	{
		try {
			readerHS = new BufferedReader(new InputStreamReader(client.getInputStream()));
			writerHS = new PrintWriter(client.getOutputStream(), true);
			
			// The next code lines are going to get the name and host from the user 
			String name = readerHS.readLine();
			String host = readerHS.readLine();
					
			// we are going to write the answer and send it to the client
			String message = "Hi "+ name + " in " + host + ", Welcome!!";
			writerHS.println(message);
			
			// we are going to close the streams and the socket associated to the request
			readerHS.close();
			writerHS.close();
			client.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}		
	}
}
