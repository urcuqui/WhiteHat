package main;
import java.net.*;
public class PruebaInetAddress {

	public static void main(String[] args) {
		// TODO Auto-generated method stub

		try 
		{
			// get the local address from the local host
			InetAddress address  = InetAddress.getLocalHost();
			System.out.println(address);
			
			// get the address from the Nasa Web server in United States 
			address = InetAddress.getByName("www.NASA.gov");
			System.out.println(address);
			
			// get the IP address from the web servers of Google 
			//InetAddress arrayAd[] = InetAddress.getAllByName("www.yahoo.com");
			InetAddress arrayAd[] = InetAddress.getAllByName("www.cali.gov.co");
			for(int i=0; i<arrayAd.length; i++)
			{
				System.out.println(arrayAd[i]);
			}
		}
		catch (java.net.UnknownHostException e) 
		{
			// TODO Auto-generated catch block
			System.out.println("Error ubicando el host");
		}				
	}
}
