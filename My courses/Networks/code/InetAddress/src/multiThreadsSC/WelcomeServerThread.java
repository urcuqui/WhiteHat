package multiThreadsSC;
import java.io.*;
import java.net.*;
public class WelcomeServerThread {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		try {
			ServerSocket server = new ServerSocket(8030);
			while(true)
			{
				Socket c = server.accept();
				ThreadWelcomeServer thread = new ThreadWelcomeServer(c);
				thread.start();
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
}
