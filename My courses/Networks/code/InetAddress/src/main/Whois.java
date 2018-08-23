package main;
import java.io.*;
import java.net.*;


public class Whois {

	public static void main(String[] args) 
	{
		// TODO Auto-generated method stub
		// the whois server name starts with the next domain
		String serverName = "whois.internic.net";
	    InetAddress server = null;
	    try 
	    {
	    	// we will use IntetAddress in order to get the address object from the server 
			server = InetAddress.getByName(serverName);
			//  we will make the socket associated to the address and the port
		    Socket theSocket = new Socket(server, 43);
		    // we will make a writer associated to the socket previously created
		    Writer out = new OutputStreamWriter(theSocket.getOutputStream());
		    out.write("mit.edu \r\n");
		    // in the next line we will send all the data in the memory
		    out.flush();
		    // in the next lines we will receive the information from the server 
		    InputStream in = new BufferedInputStream(theSocket.getInputStream());
		    int c;
			    while ((c = in.read()) != -1)
			    {
			      System.out.write(c);
			    }
			// the next close process is necessary
			theSocket.close();
			in.close();
			in.close();
		 
	    } catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
