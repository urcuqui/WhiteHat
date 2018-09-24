package multiThreadsSC;
import java.net.*;
import java.io.*;
public class RunnableWelcomeServerThread implements Runnable
{
	Socket client;
	BufferedReader readerHS;
	PrintWriter writerHS;
	
	public RunnableWelcomeServerThread(Socket request)
	{
		super();
		client = request;
	}
	public void run()
	{		
		try 
		{
			// the next lines are going to make the streams associated 
			readerHS = new BufferedReader(new InputStreamReader(client.getInputStream()));
			writerHS = new PrintWriter(client.getOutputStream(),true);
			
			// we are going to get the name and host from the user
			String name =  readerHS.readLine();
			String host =  readerHS.readLine();
			
			// we are going to make the answer and the send it to the client
			String message = "Hi " + name + " in "+ host + ", Welcome!!!";
			writerHS.println(message);
			
			// the next code lines are going to close the streams and the socket associated to the request
			readerHS.close();
			writerHS.close();
			client.close();
			
			
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
