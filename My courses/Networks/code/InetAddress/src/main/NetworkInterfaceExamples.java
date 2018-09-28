package main;

import java.net.*;
import java.util.*;
/**
 * This is the code of the NetworkInterface examples of the book:
 * Hughes, M., Shoffner, M., Hamner, D., Winslow, M., & Hughes, C. (1997). 
 * Java network programming (Vol. 2). Greenwich/CT: Manning.
 * @author 	Christian Urcuqui
 * [0][1][0]
 * [0][0][1] 
 * [1][1][1]
 */
public class NetworkInterfaceExamples {

	private static Scanner scanner;

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		System.out.println("Write the number of the example to execute: ");		
		scanner = new Scanner(System.in);
		// I'm going to get the number of the example that I want to show
		int example = scanner.nextInt();
		switch(example)
		{
			case 1:
				exampleOne();
				break;
			case 2:
				exampleTwo();
				break;
			case 3:
				exampleThree();
				break;
			case 4:
				break;
				
		};
			
	}
	
	
	public static void exampleOne()
	{
		try
		{
			InetAddress local = InetAddress.getByName("127.0.0.1");
			NetworkInterface ni = NetworkInterface.getByInetAddress(local);
			if(ni == null)
			{
				System.err.println("That's weird. No cal loopback address.");				
			}
			else
			{
				System.out.println(ni.getName());
			}
		} catch (SocketException ex)
		{
			System.err.println("Could not list network interfaces.");
		} catch (UnknownHostException ex)
		{
			System.err.println("That's weird. Could not lookup 127.0.0.1");
		}
	}
	
	/**
	 * This is the example that allows us to understand the use of getNetworkInterfaces
	 */
	public static void exampleTwo()
	{
		Enumeration<NetworkInterface> interfaces;
		try {
			interfaces = NetworkInterface.getNetworkInterfaces();
			while(interfaces.hasMoreElements())
			{
				NetworkInterface ni = interfaces.nextElement();
				System.out.println(ni);
				Enumeration<InetAddress> addresses = ni.getInetAddresses();

			      while( addresses.hasMoreElements() )
			      {
			        InetAddress addr = addresses.nextElement();
			        if( addr instanceof Inet4Address && !addr.isLoopbackAddress() )
			        {
			          System.out.println(addr);
			        }
			      }
			}
		} catch (SocketException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		main(null);
	}
	
	/**
	 * A enumeration object has a InetAddress object for each IP address the interface is bound to.
	 */
	public static void exampleThree()
	{
		// the next line only will be useful if we have an interface name with "eth0" (commonly used in UNIX systems)
		// if we want to analyze this example in a windows environment we can use the "lo" interface
		NetworkInterface eth0;
		try {
			// Windows
			//eth0 = NetworkInterface.getByName("lo");
			// UNIX
			//eth0 = NetworkInterface.getByName("eth0");
			scanner.nextLine();
			System.out.println("Write the interfaz name");
			String name = scanner.nextLine();
			if(name != null)
			{
				System.out.println(name);
				eth0 = NetworkInterface.getByName(name);
				Enumeration <InetAddress>addresses = eth0.getInetAddresses();
			    while(addresses.hasMoreElements() )
			    {
					InetAddress addr =  addresses.nextElement();
					if( addr instanceof Inet4Address && !addr.isLoopbackAddress() )
					{
				      System.out.println("IPv4 or loopback");
					  System.out.println(addr);
					}
					if (addr instanceof Inet6Address)
					{
						System.out.println("IPv6");
						System.out.println(addr);
					}
			    }	
			}					
		} catch (SocketException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		main(null);		
	}
	
	

}
