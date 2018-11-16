package web;


import java.io.IOException;
import java.net.*;

public class WebServerHack1 {

	public WebServerHack1()
	{
		System.out.println("Webserver Started");
		try {
			ServerSocket serverSocket =  new ServerSocket(80);
			while(true) 
			{
				System.out.println("Waiting for the client request");
				Socket remote = serverSocket.accept();
				System.out.println("Connection made");
				new Thread(new ClientHandlerHack1(remote)).start();
				
			}
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		new WebServerHack1();
	}
}
