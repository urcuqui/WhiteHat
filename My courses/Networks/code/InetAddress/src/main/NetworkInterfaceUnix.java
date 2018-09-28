package main;
import java.net.*;
public class NetworkInterfaceUnix {
	
	public static void main(String[] args) 
	{
		try
		{
			NetworkInterface ni =  NetworkInterface.getByName("eth0");
			if(ni == null)
			{
				System.err.println("No such interface: eth0");
			}
		} catch(SocketException ex)
		{
			System.err.println("Could not list sockets.");
		}	
	}
}
	

