package InetAddress;

import java.net.Inet4Address;
import java.net.InetAddress;
import java.net.UnknownHostException;

public class Ejemplo_InetAddress {
	
	
	public static void main(String[] args) {
		
		try {
			System.out.println("::Devuelve la dir IP del nombre de la maquina escrito como param::");
			System.out.println(Inet4Address.getByName("localhost"));
			System.out.println("---------------------------");
			System.out.println("::Devuelve la dir IP asociada a este HOST::");
			System.out.println(Inet4Address.getLocalHost());
			System.out.println("---------------------------");
			System.out.println("::Devuelve las dir IP asociada a este HOST::");
			InetAddress[] temp = Inet4Address.getAllByName("localhost");
			for (int i = 0; i < temp.length; i++) {
				
				System.out.println(Inet4Address.getByName(temp[i].getHostAddress()));
				
			}		
			
			System.out.println("---------------------------");

			System.out.println("---------------------------");

			System.out.println("---------------------------");
			System.out.println("::Host::");
			//www.yahoo.es , www.google.es
			System.out.println(InetAddress.getByName("www.yahoo.es"));
			System.out.println("::IP::");
			System.out.println(InetAddress.getByName("www.yahoo.es").getHostAddress());
			System.out.println("::NOMBRE::");
			System.out.println(InetAddress.getByName("www.yahoo.es").getHostName());
			System.out.println("---------------------------");

			System.out.println("---------------------------");

			System.out.println("---------------------------");
			
			
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		
		
		
		
		
		
		
		
		
	}
	
	
	
	

}
