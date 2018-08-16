package main;
import java.net.*;
public class BytesAddress {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		InetAddress address;
		try {
			address = InetAddress.getByName("www.nasa.gov");
			System.out.println(address);
			// In order to get the bytes from the address
			byte[] add = address.getAddress();
			System.out.println("Address in bytes");
			String result = "";
			for(int i=0; i<add.length; i++)
			{
				result += add[i]+ ".";
							
			}
			System.out.println(result);	
			System.out.println("\nAddress in decimal notation");
			// In order to change the bytes address to decimal values
			int value;
			result = "";
			for(int i=0; i<add.length; i++)
			{
				value = 0xff & add[i];
				// https://www.mkyong.com/java/java-and-0xff-example/
				// 0xff & is used to get the last 8 bits 
				result += value+ ".";				
			}
			System.out.println(result);				
			
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}			
	}
}
