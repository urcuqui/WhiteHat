package main;
import java.net.*;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
public class DataHosts {

	
		static char ipClass(byte[] ip)
		{
			int highByte = 0xff & ip[0];
			return (highByte <128)
					?'A'
					:(highByte <192)
					?'B'
					:(highByte <224)
					?'C'
					:(highByte <240)
					?'D'
					:'E';
		}
		static void localAddress()
		{
			try {
				InetAddress local = InetAddress.getLocalHost();
				System.out.println("The name of the local host is: "+local.getHostName());
				System.out.println("IP address: "+local.getHostAddress());
				System.out.println("IP class: "+ ipClass(local.getAddress()));
			} catch (UnknownHostException e) {
				// TODO Auto-generated catch block
				System.out.println("We can't reach the host");
			}			
		}
		static void remoteAddress(String name)
		{
			System.out.println("Searching "+name+"...");
			try {
				InetAddress host = InetAddress.getByName(name);
				System.out.println("Host name: "+ host.getHostName());
				System.out.println("IP host: "+ host.getHostAddress());
				System.out.println("Class of the host: "+ ipClass(host.getAddress()));
			} catch (UnknownHostException e) {
				// TODO Auto-generated catch block
				System.out.println("We can't reach " + name);
			}
			
		}
		
	public static void main(String[] args) {
		// TODO Auto-generated method stub
		localAddress();
		BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        System.out.print("Enter the ID of the host" );        
        // example 8.8.8.8 the Google public DNS 
        
        try {
			try {
				String s = br.readLine();
				remoteAddress(s);
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		} catch (NumberFormatException e) {
			// TODO Auto-generated catch block
			System.err.println("Invalid Format!");
		}
        
	}

}
