package webserver_logs;

import java.net.*;
import java.util.concurrent.Callable;
/**
 * This class implements Callable and it parses a logfile entry, looks up a single address, and
 * replaces that address with the corresponding hostname
 * @author Christian Urcuqui
 *
 */
public class LookupTask implements Callable<String>
{

	private String line;
	public LookupTask(String line) 
	{
		this.line = line;
	}
	
	@Override
	public String call() throws Exception {
		// TODO Auto-generated method stub
		try 
		{
			// separate out the IP address
			int index = line.indexOf(' ');
			String address = line.substring(0, index);
			String theRest = line.substring(index);
			String hostname = InetAddress.getByName(address).getHostName();
			return hostname + " " + theRest;
		} catch (Exception ex) 
		{
			return line;
		}
	}

}
