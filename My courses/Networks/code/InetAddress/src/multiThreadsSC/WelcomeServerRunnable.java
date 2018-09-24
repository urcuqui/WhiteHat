package multiThreadsSC;
import java.io.*;
import java.net.*;
public class WelcomeServerRunnable {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		ServerSocket server;
		try {
			server = new ServerSocket(8030);
			while(true)
			{
				Socket c = server.accept();				
				Thread thread = new Thread(new RunnableWelcomeServerThread(c));
				thread.start();
			}
		} catch (IOException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
		
	}

}
