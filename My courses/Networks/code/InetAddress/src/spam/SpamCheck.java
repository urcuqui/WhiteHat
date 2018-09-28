package spam;
import java.net.*;
import java.util.*;


/**
 * This is a Spammer check example from the book:
 * Hughes, M., Shoffner, M., Hamner, D., Winslow, M., & Hughes, C. (1997). 
 * Java network programming (Vol. 2). Greenwich/CT: Manning.
 * @author 	Christian Urcuqui
 * [0][1][0]
 * [0][0][1] 
 * [1][1][1]
 */
public class SpamCheck {

	//https://www.spamhaus.org/faq/section/DNSBL%2520Usage#200
	public static final String BLACKHOLDE = "sbl.spamhaous.org";
	public static final String BLACKHOLDE_2 = "pbl.spamhaous.org";
	public static final String BLACKHOLDE_3 ="xbl.spamhaus.org";
	
	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		
		Scanner scanner = new Scanner(System.in);
		String input = "";
		// I'm going to get the number of the example that I want to show
		do
		{
			System.out.println("Write the IP to analyze");
			input = scanner.nextLine();
			if(isSpammer(input))
			{
				System.out.println(input + " is a known spammer.");
			}
			else
			{
				System.out.println(input + " appears legitimate");
			}
		}while(input.equals("exit")==false);
		
			/*for (String arg:args)
			{
				if(isSpammer(arg))
				{
					System.out.println(arg + " is a known spammer.");
				}
				else
				{
					System.out.println(arg + " appears legitimate");
				}
			}*/
	}
	
	private static boolean isSpammer(String arg)
	{
		InetAddress address;
		try {
			address = InetAddress.getByName(arg);
			byte[] quad =  address.getAddress();
			String query = BLACKHOLDE;
			String query2 = BLACKHOLDE_2;
			String query3 = BLACKHOLDE_3;
			for(byte octet: quad)
			{
				int unsignedByte = octet < 0 ? octet + 256 : octet;
				query = unsignedByte + "." + query;				
			}
			for(byte octet: quad)
			{
				int unsignedByte = octet < 0 ? octet + 256 : octet;
				query2 = unsignedByte + "." + query2;				
			}
			for(byte octet: quad)
			{
				int unsignedByte = octet < 0 ? octet + 256 : octet;
				query3 = unsignedByte + "." + query3;				
			}
			System.out.println(query3);
			InetAddress.getByName(query);
			InetAddress.getByName(query2);			
			InetAddress.getByName(query3);
			return true;
		} catch (UnknownHostException e) {
			// TODO Auto-generated catch block
			return false;
		}
		
	}

}
