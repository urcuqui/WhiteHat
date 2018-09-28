package webserver_logs;
import java.io.*;
import java.net.*;
import java.util.*;
/** 
 * @author Christian Urcuqui
 * [0][1][0]
 * [0][0][1] 
 * [1][1][1]
 * This class allows us to print the hostname associated to each IP in a log file
 * This is the first example of to analyze the logs from the book:
 * Hughes, M., Shoffner, M., Hamner, D., Winslow, M., & Hughes, C. (1997). 
 * Java network programming (Vol. 2). Greenwich/CT: Manning.
 */
public class Weblog {

	public static void main(String[] args) {
		// TODO Auto-generated method stub
		Scanner scanner = new Scanner(System.in);
		String dir = "";
		do
		{
			System.out.println("Write the path of the log file");
			dir = scanner.nextLine();
			try {
				
				// these lines get the log file 
				FileInputStream fin = new FileInputStream(dir);
				Reader in = new InputStreamReader(fin);
				BufferedReader bin = new BufferedReader(in);
				
				// the next loop places one line in the String variable entry. entry is then split into two substring (IP and theRest)
				for(String entry = bin.readLine(); entry!=null; entry = bin.readLine())
				{
					// Separate out the IP address
					int index = entry.indexOf(' ');					
					String ip = entry.substring(0, index);
					String theRest = entry.substring(index);
					
					try {
					// Ask DNS for the hostname and it out					
					InetAddress address = InetAddress.getByName(ip);
					System.out.println(address.getHostName() + theRest);
					}
					catch (UnknownHostException ex) 
					{
						System.err.println(entry);
					}					
				}
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} 
					
					
					
		}while(dir.equals("exit")==false);
		
		
	}

}
